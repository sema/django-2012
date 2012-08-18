from git import GitCmdObjectDB, Repo
import gitmanager
import unittest
import shutil
import os

class Test(unittest.TestCase):
    
    def setUp(self):
        # TODO make repositories portable...
        here = os.path.abspath(os.path.dirname(__file__))
        testdata = here + "/testdata" 
        self.url = testdata + "/testrepository"
        self.live_url = 'https://github.com/sema/navtree.git'
        self.live_url_dir = testdata + "/live_repo"
        self.scraper = gitmanager.GitManager() 

    def test_scrape_single(self):
        repo = Repo(self.url, odbt=GitCmdObjectDB)
        commit = list(repo.iter_commits())[0]
        activity = self.scraper._commit2activity(url="someurl", commit=commit)
        self.assertIsNotNone(activity)
        self.assertIsNotNone(activity.url)
        self.assertIsNotNone(activity.login)
        self.assertIsNotNone(activity.date)
    
    def test_scrape_multi(self):
        activities = self.scraper._repo2activities(Repo(self.url, odbt=GitCmdObjectDB), self.url)
        self.assertTrue(activities)
    
    def test_scrape_partial(self):
        '''
        tries to get just the 5 most recent commits. 
        
        This is done by finding the date for the 6th most recent commit.
        And quering for that time. 
        '''
        full = self.scraper._repo2activities(Repo(self.url, odbt=GitCmdObjectDB), self.url)
        self.assertTrue(full)
        partial = self.scraper._repo2activities(Repo(self.url, odbt=GitCmdObjectDB), self.url,
                                               full[5].date)
        self.assertTrue(partial)
        self.assertGreater(len(full), len(partial))
        self.assertEqual(5, len(partial))
     
    def test_clone(self):
        clone_url = self.live_url
        repo_dir = self.live_url_dir
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)
        os.mkdir(repo_dir)
        repo = self.scraper._clone_and_get_repo(clone_url, repo_dir)
        self.assertIsNotNone(repo)
    
    def test_can_pull(self):
        self.scraper._pull(Repo(self.live_url_dir))
    
    def test_repository_naming(self):
        url = "foobarbaz"
        location = self.scraper._get_repository_location(url)
        self.assertTrue(location)     
        self.assertFalse("foobarbaz" in location)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTest']
    unittest.main()
