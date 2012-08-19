'''
Created on Aug 19, 2012

@author: esbena
'''
import os
import unittest
import mercurialmanager
from hgapi import Repo
import shutil
here = os.path.abspath(os.path.dirname(__file__))
testdata = here + "/testdata" 
local_url = testdata + "/testrepository"
scraper = mercurialmanager.MercurialManager(testdata)
live_url = 'https://bitbucket.org/dahlia/bitbucket-distutils'
live_url_dir = scraper._get_repository_location(live_url)

class Test(unittest.TestCase):
    def test_scrape_single(self):
        repo = Repo(local_url)
        commit = list(repo.revisions(slice(0, 1)))[0]
        activity = scraper._commit2activity(commit=commit)
        self.assertIsNotNone(activity)
        self.assertIsNotNone(activity.login)
        self.assertIsNotNone(activity.date)
    
    def test_scrape_multi(self):
        activities = scraper._repo2activities(Repo(local_url))
        self.assertTrue(activities)
    
    def test_scrape_partial(self):
        '''
        tries to get just the 5 most recent commits. 
        
        This is done by finding the date for the 6th most recent commit.
        And quering for that time. 
        '''
        full = scraper._repo2activities(Repo(local_url))
        self.assertTrue(full)
        partial = scraper._repo2activities(Repo(local_url),
                                               full[1].date)
        self.assertTrue(partial)
        self.assertGreater(len(full), len(partial))
        self.assertEqual(2, len(partial))
     
    def test_clone(self):
        clone_url = live_url
        repo_dir = live_url_dir
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)
        os.mkdir(repo_dir)
        repo = scraper._clone_and_get_repo(clone_url, repo_dir)
        self.assertIsNotNone(repo)
    
    def test_can_update(self):
        scraper._update(local_url)
    
    def test_repository_naming(self):
        url = "foobarbaz"
        location = scraper._get_repository_location(url)
        self.assertTrue(location)     
        self.assertFalse("foobarbaz" in location)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
