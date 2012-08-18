from datetime import timedelta, datetime
from git import GitCmdObjectDB, Repo

class SimpleActivity(object):
    '''
    Simple wrapper object for a commit.
    '''
    def __init__(self, date, login, url):
        self.date = date
        self.login = login
        self.url = url

class GitManager(object):
    '''
    Manages a git repository.
    
    Is able to checkout and pull from the remote git repository.
    
    Only checks the git related metadata files out.
    
    Is able to read the history of the repository. 
    '''

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
    
    def repo2activities(self, url, since=None):
        """
        Reads the complete history of the repository at the specified url.
        Optionally, only the history since a certain date is read. 
        """
        repo = Repo(url, odbt=GitCmdObjectDB)
        commits = repo.iter_commits()
        simple_activities = [self._commit2activity(commit, url) for commit in commits]
         
        if since:
            # TODO make git-python use the 'since' arg instead!??!
            return [recent for recent in simple_activities if recent.date > since] 
        else:
            return simple_activities
        
         
    def pull(self, repo):
        """
        Pulls the repository at the specified url
        """
        repo.remote().pull()
        
    def clone_and_get_repo(self, clone_url, location):
        """
        Performs the initial checkout of a repository at the specified url.
        Returns the fresh repository.
        """
        from subprocess import call
        # TODO git api does not work here?!
        # TODO security
        call(["git", "clone", "--no-checkout", clone_url, location])
        return Repo(location)
