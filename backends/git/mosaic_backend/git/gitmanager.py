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

    def __init__(self):
        self.repository_directory = "repositories"
        self.concrete_activity_type = 'git'
        self.abstract_activity_type = 'repository'
        logger.debug("Initialized GitManager")

    def _to_dict(self, activity):
        {'url': activity.url, 'date': activity.date, 'login': activity.login}

    def _get_repository_location(self, url):
        '''
        Creates the absolute path of the repository with the given url
        '''
        import base64
        if not os.path.exists(self.repository_directory):
            os.mkdir(self.repository_directory)
        # for safety
        repo_dir_name = base64.urlsafe_b64encode(url)
        return "%s/%s" % (self.repository_directory, repo_dir_name)
        
    def _has_repository(self, url):
        '''
        Decides if the repository for an url exists locally
        '''
        return os.path.exists(self._get_repository_location(url))
    
    def _repository_is_stale(self, repo, threshold=None):
        '''
        Decides wether the a repository is stale and needs an update
        '''
        if not threshold:
            threshold = datetime.timedelta(hours=24)
        commit = repo.commit()
        if not commit:
            return True
        last_commit = datetime.fromtimestamp(commit.committed_date)
        time_since_last_commit = (datetime.now() - last_commit)
        return time_since_last_commit > threshold         
    
    def get_activities(self, url, since):
        '''
        Gets all activities for a repository at a url since some date.
        
        Might clone og pull from remote repositories.
        '''
        location = self._get_repository_location(url)
        if not self._has_repository_at_location(location):
            self._clone_and_get_repo(url, location)
        repo = Repo(location, odbt=GitCmdObjectDB)
        if self._repository_is_stale(repo):
            self._pull(repo)
        return [self._to_dict(a) for a in
                    self._repo2activities(repo, url, since)]
          
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
            simple_activities = [recent for recent in simple_activities if recent.date > since]
        return simple_activities
        
         
    def _pull(self, repo):
        """
        Pulls the specified repository 
        """
        logger.info("Pulling from %s" % repo)
        repo.remote().pull()
        
    def _clone_and_get_repo(self, clone_url, location):
        """
        Performs the initial checkout of a repository at the specified url.
        Returns the fresh repository.
        """
        from subprocess import call
        # TODO git api does not work here?!
        logger.debug("Cloning from %s to %s" % (clone_url, location))
        call(["git", "clone", "--no-checkout", clone_url, location])
        logger.info("Cloned from %s to %s" % (clone_url, location))
        return Repo(location)
