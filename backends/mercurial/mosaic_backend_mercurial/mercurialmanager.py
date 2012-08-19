from hgapi.hgapi import Repo
from mosaic_backend.activity import SimpleActivity
from datetime import datetime, timedelta
from dateutil import parser
import logging
import os

logger = logging.getLogger(__name__)

class MercurialManager(object):
    '''
    Manages a mercurial repository.
    
    Is able to checkout and pull from the remote mercurial repository.
    
    Only checks the mercurial related metadata files out.
    
    Is able to read the history of the repository. 
    '''
    def __init__(self, repository_directory):
        self.repository_directory = repository_directory
        self.concrete_activity_type = 'hg'
        self.abstract_activity_type = 'repository'
        logger.debug("Initialized MercurialManager")
 
    def _to_dict(self, activity):
        import time
        return {'date': time.mktime(activity.date.timetuple()), 'login': activity.login}
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
        return os.path.exists("%s/%s" % (self._get_repository_location(url), ".hg"))
    
    def get_activities(self, url, since):
        '''
        Gets all activities for a repository at a url since some date.
        
        Might clone og pull from remote repositories.
        '''
        try:
            location = self._get_repository_location(url)
            if not self._has_repository(url):
                self._clone_and_get_repo(url, location)
            repo = Repo(location)
            self._update(location)
            return [self._to_dict(a) for a in
                        self._repo2activities(repo, since)]
        except Exception as e:
            logger.exception(e)
            return []
          
    def _get_commit_time(self, commit):
        '''
        Takes care of time zones.
        '''
        return parser.parse(commit.date)
        
    def _commit2activity(self, commit):
        """
        Simple mapping function
        """
        activity = SimpleActivity(date=self._get_commit_time(commit),
                login=commit.author)
        return activity

    def _repo2activities(self, repo, since=None):
        """
        Reads the complete history of the repository at the specified repository.
        Optionally, only the history since a certain date is read. 
        """
        commits = repo.revisions(slice(0,-1))
        simple_activities = [self._commit2activity(commit) for commit in commits]
        
        if since:
            logger.debug("filtering %d activities: " % len(simple_activities))
            simple_activities = [recent for recent in simple_activities if recent.date > since]
        
        logger.debug("found %d activities: " % len(simple_activities))
        return simple_activities
         
    def _update(self, location):
        """
        Updates the specified repository 
        """
        from subprocess import call
        logger.info("pulling from %s:" % location)
        exit_status = call(["hg", "pull", location])
        
        if exit_status == 0:
            logger.info("Update %s" % location)
        else:
            raise Exception("Update failed: %s" % location);
        
        
    def _clone_and_get_repo(self, clone_url, location):
        """
        Performs the initial checkout of a repository at the specified url.
        Returns the fresh repository.
        """
        from subprocess import call
        logger.debug("Cloning from %s to %s" % (clone_url, location))
        exit_status = call(["hg", "clone", "--noupdate", clone_url, location])
        
        if exit_status == 0:
            logger.info("Cloned from %s to %s" % (clone_url, location))
        else:
            raise Exception("Failed to clone from %s to %s" % (clone_url, location));

        return Repo(location)       
