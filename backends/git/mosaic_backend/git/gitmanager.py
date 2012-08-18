from datetime import timedelta, datetime
from git import GitCmdObjectDB, Repo
from mosaic_backend.worker import SimpleActivity
import logging
import os
logger = logging.getLogger(__name__)
class GitManager(object):
    '''
    Manages a git repository.
    
    Is able to checkout and pull from the remote git repository.
    
    Only checks the git related metadata files out.
    
    Is able to read the history of the repository. 
    '''

    def __init__(self, repository_directory):
        self.repository_directory = repository_directory
        self.concrete_activity_type = 'git'
        self.abstract_activity_type = 'repository'
        logger.debug("Initialized GitManager")

    def _to_dict(self, activity):
        import time
        return {'url': activity.url, 'date': time.mktime(activity.date.timetuple()), 'login': activity.login.email}

    def _get_repository_location(self, url):
        '''
        Creates the absolute path of the repository with the given url
        '''
        import base64
        if not os.path.exists(self.repository_directory):
            os.mkdir(self.repository_directory)
        # for safety
        repo_dir_name = base64.urlsafe_b64encode(url)
        full_path = "%s/%s" % (self.repository_directory, repo_dir_name)
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        return full_path

        
    def _has_repository(self, url):
        '''
        Decides if the repository for an url exists locally
        '''
        return os.path.exists("%s/%s" % (self._get_repository_location(url), ".git"))
       
    def get_activities(self, url, since):
        '''
        Gets all activities for a repository at a url since some date.
        
        Might clone og pull from remote repositories.
        '''
        try:
            location = self._get_repository_location(url)
            if not self._has_repository(url):
                self._clone_and_get_repo(url, location)
            repo = Repo(location, odbt=GitCmdObjectDB)
            self._pull(repo)
            return [self._to_dict(a) for a in
                        self._repo2activities(repo, url, since)]
        except Exception as e:
            logger.exception(e)
            return []
          
    def _get_commit_time(self, commit):
        '''
        Takes care of time zones.
        '''
        delta = timedelta(seconds=commit.committer_tz_offset)
        date = datetime.fromtimestamp(commit.committed_date)
        utc_date = date + delta
        return utc_date
        
    def _commit2activity(self, commit, url):
        """
        Simple mapping function
        """
        activity = SimpleActivity(date=self._get_commit_time(commit),
                login=commit.committer,
                url=url)
        return activity

    # TODO remove redundant url requirement, it should be extractable from repo?     
    def _repo2activities(self, repo, url, since=None):
        """
        Reads the complete history of the repository at the specified repository.
        Optionally, only the history since a certain date is read. 
        """
        commits = repo.iter_commits()
        simple_activities = [self._commit2activity(commit, url) for commit in commits]
        
        if since:
            # TODO make git-python use the 'since' arg instead!??!
            logger.debug("filtering %d activities: " % len(simple_activities))
            simple_activities = [recent for recent in simple_activities if recent.date > since]
        
        logger.debug("found %d activities: " % len(simple_activities))
        return simple_activities
        
         
    def _pull(self, repo):
        """
        Pulls the specified repository 
        """
        remote = repo.remote()
        repo.remote().pull()
        # TODO make branches work?
#        for ref in remote.refs:
#            logger.debug("ref.name: %s" % ref.name)
#            branch = ref.name.split("/")[1]
#            repo.remote().pull(branch)
        
        
    def _clone_and_get_repo(self, clone_url, location):
        """
        Performs the initial checkout of a repository at the specified url.
        Returns the fresh repository.
        """
        from subprocess import call
        # TODO git api does not work here?!
        logger.debug("Cloning from %s to %s" % (clone_url, location))
        exit = call(["git", "clone", "--no-checkout", clone_url, location])
        
        if exit == 0:
            logger.info("Cloned from %s to %s" % (clone_url, location))
        else:
            raise Exception("Failed to clone from %s to %s" % (clone_url, location));

        return Repo(location)
