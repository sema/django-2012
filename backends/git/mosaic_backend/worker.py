import json
import time
import urllib2
import logging
class SimpleActivity(object):
    '''
    Simple wrapper object for a commit.
    '''
    def __init__(self, date, login, url,):
        self.date = date
        self.login = login
        self.url = url

logger = logging.getLogger(__name__)
class Worker(object):
    
    '''
    Generic worker class. Will periodically do work for the MOSAiC server when instantiated with an 'activity manager'.
    '''
    
    def __init__(self, mosaic_url, manager):
        '''
        Constructs a worker for the MOSAiC server at the specified URL.
        The supplied manager should specify its capabilities regarding
        activity types through the properties, concrete_activity_type and abstract_activity_type:
        ex.:      
        concrete_activity_type = 'git'
        abstract_activity_type = 'repository'
        
        The manager should also be able to perform work when requested to: 
        A method: get_activies(url, since) : [activity-dict] is required 
      
        '''
        self.manager = manager
        common_path = "%s/worklist/%s/%s" % (mosaic_url, manager.abstract_activity_type, manager.concrete_activity_type)
        self.get_url = common_path 
        self.post_url = "%s/deliver" % common_path
        logger.info("Initialized worker for %s" % common_path)
    
    def run(self, sleep_time=5):
        '''
        main loop for performing work for the MOSAiC server
        '''
        while(True):
            work_list = self._get_work()
            logger.info("Received work_list of size: %s" % len(work_list))
            logger.debug("Received work_list: %s", work_list)
            for work in work_list:
                url = work['url']
                since = work['since']
                activities = self.manager.get_activities(url, since)
                logger.debug("Delivering work: %s", activities)
                self._deliver_work(activities)
            time.sleep(sleep_time)
    
    def _get_work(self):
        '''
        Requests work from the MOSAiC server
        '''        
        data = urllib2.urlopen(self.get_url)
        json_data = json.load(data)
        print("%s -> %s" % (self.get_url, json_data))
        return json_data   
        
    def _deliver_work(self, activities):
        '''
        Delivers completed work to the MOSAiC server
        '''
        json_data = json.dumps(activities)
        print("%s <- %s" % (self.post_url, json_data))
        #urllib2.urlopen(self.post_url, json_string)

