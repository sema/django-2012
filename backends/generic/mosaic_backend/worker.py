from urllib2 import HTTPError
import datetime
import json
import logging
import time
import urllib
import urllib2
from symbol import except_clause


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
        api_key = "SUPER_SECRET"
        self.manager = manager
        parameters = urllib.urlencode({'token': api_key})
        common_path = "%s/api/worklist/%s/%s" % (mosaic_url, manager.abstract_activity_type, manager.concrete_activity_type)
        self.get_url = "%s?%s" % (common_path,parameters)  
        self.post_url = "%s/deliver/?%s" % (common_path, parameters)
        logger.info("Initialized worker for %s" % common_path)
    
    def run(self, sleep_time=5):
        '''
        main loop for performing work for the MOSAiC server
        '''
        import sys
        while(True):
            try:
                work_list = self._get_work()
                logger.info("Received work_list of size: %s" % len(work_list))
                logger.debug("Received work_list: %s", work_list)
                for work in work_list:
                    url = work['url']
                    since = work['since']
                    if since:
                        since = datetime.datetime.fromtimestamp(since)
                    activities = self.manager.get_activities(url, since)
                    logger.debug("Delivering work: %s", activities)
                    self._deliver_work(activities, url)
                time.sleep(sleep_time)
            except Exception as e:
                logger.exception(e)
                time.sleep(sleep_time * 10)
    
    def _get_work(self):
        '''
        Requests work from the MOSAiC server
        '''
        try:
            data = urllib2.urlopen(self.get_url)
        except HTTPError:
            logger.error(("Failed to open url: %s" % str(self.get_url)))
            return []
        
        json_data = json.load(data)
        logger.info("%s -> %s" % (self.get_url, json_data))
        return json_data   
        
    def _deliver_work(self, activities, url):
        '''
        Delivers completed work to the MOSAiC server
        '''
        json_data = json.dumps({'activities': activities, 'url': url})
        logger.info("%s <- %s" % (self.post_url, json_data))
        try:
            urllib2.urlopen(self.post_url, urllib.urlencode({'payload': json_data}))
        except HTTPError:
            logger.error("Failed to open url: %s" % str(self.post_url))

