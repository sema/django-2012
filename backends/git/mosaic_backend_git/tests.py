from git import GitCmdObjectDB, Repo
import gitmanager
import unittest
import shutil
import os

testdata = os.path.abspath(os.path.dirname(__file__)) + "/testdata" 
local_url = testdata + "/testrepository"
live_url = 'https://github.com/sema/navtree.git'
scraper = gitmanager.GitManager(testdata) 
class Test(unittest.TestCase):
        
    def test_scrape_single(self):
        repo = Repo(local_url, odbt=GitCmdObjectDB)
        commit = list(repo.iter_commits())[0]
        activity = scraper._commit2activity(commit=commit)
        self.assertIsNotNone(activity)
        self.assertIsNotNone(activity.login)
        self.assertIsNotNone(activity.date)
    
    def test_scrape_multi(self):
        activities = scraper._repo2activities(Repo(local_url, odbt=GitCmdObjectDB))
        self.assertTrue(activities)
    
    def test_scrape_partial(self):
        '''
        tries to get just the 5 most recent commits. 
        
        This is done by finding the date for the 6th most recent commit.
        And quering for that time. 
        '''
        full = scraper._repo2activities(Repo(local_url, odbt=GitCmdObjectDB))
        self.assertTrue(full)
        partial = scraper._repo2activities(Repo(local_url, odbt=GitCmdObjectDB),
                                               full[5].date)
        self.assertTrue(partial)
        self.assertGreater(len(full), len(partial))
        self.assertEqual(5, len(partial))
     
    def test_clone(self):
        clone_url = live_url
        repo_dir = scraper._get_repository_location(live_url)
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)
        os.mkdir(repo_dir)
        repo = scraper._clone_and_get_repo(clone_url, repo_dir)
        self.assertIsNotNone(repo)
    
    def test_can_pull(self):
        scraper._pull(Repo(local_url))
    
    def test_repository_naming(self):
        url = "foobarbaz"
        location = scraper._get_repository_location(url)
        self.assertTrue(location)     
        self.assertFalse("foobarbaz" in location)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTest']
    unittest.main()
