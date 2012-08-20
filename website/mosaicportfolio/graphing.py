from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from mosaicportfolio.models import RepositoryActivity, Repository, \
    ProjectRepository
import logging
logger = logging.getLogger(__name__)

def get_activities_for_project_repository(prep):
    return RepositoryActivity.objects.filter(repository=prep.repository).filter(login=prep.login)

def make_user_graph(user):
    '''
    Creates a Graph for all the activities of all the projects of a user.
    '''
    project_repositories = ProjectRepository.objects.filter(project__user=user)
    grouped_activities = {}
    for prep in project_repositories:
        if not grouped_activities.has_key(prep.project.name):
            grouped_activities[prep.project.name] = []
        grouped_activities[prep.project.name].extend(get_activities_for_project_repository(prep))
    return Graph(_("Activity graph"), TableData(grouped_activities)).to_dict()

def make_project_graph(project):
    '''
    Creates a Graph for all the activities of a project.
    '''
    project_repositories = ProjectRepository.objects.filter(project=project)
    activities = []
    for prep in project_repositories:
        activities.extend(get_activities_for_project_repository(prep))
    grouped_activities = {}
    grouped_activities[project.name] = activities
    return Graph(_("Activity graph"), TableData(grouped_activities)).to_dict()

class Graph(object):
    '''
    The data required for constructing a Google Chart graph. 
    '''
    
    def __init__(self, title, table):
        '''
        Creates a graph with the desired title, based on the content of a Table. 
        '''
        self.title = title
        self.table = table
    
    def to_dict(self):
        return {'title': self.title, 'vTitle': _("Activities"), 'hTitle': _('Time'), 'table': self.table.to_list()}
     
class TableData(object):
    '''
    Class for grouping and transforming a collection of activities into a Google Charts compatible format.
    '''
    
    def __init__(self, grouped_actitivies):
        '''
        
        '''
        self.grouped_actitivies = grouped_actitivies
    
    def to_list(self):
        '''
        Complex implementation: calculates the total number of activities per year-month tuple,
         and outputs the result in a list-of-lists which represents a table.
        '''

        # TODO instead of grouping here, Google Charts can group for us?!
        
        # dict: {(year, month): {name: count})
        yearmonth_name_count = {}
        names = self.grouped_actitivies.keys()
        for name, activities in self.grouped_actitivies.items():
            for activity in activities:
                year = activity.date.year
                month = activity.date.month
                key = (year, month)
                if not yearmonth_name_count.has_key(key):
                    yearmonth_name_count[key] = {}
                name_count = yearmonth_name_count[key]
                name_count[name] = name_count.get(name, 0) + 1

        #ensure consistent ordering
        name_order = sorted(names)
        yearmonth_order = sorted(yearmonth_name_count.keys())
        # build the table, each row will have the same length
        table = []
        header = [_('Time')]
        header.extend(name_order)
        table.append(header)
        for yearmonth in yearmonth_order:
            row = []
            # TODO use a date, and let Google Charts do magic
            row.append("%s/%s" % (yearmonth[0], yearmonth[1]))
            for name in name_order:
                coordinate_value = yearmonth_name_count.get(yearmonth, {}).get(name, 0)
                row.append(coordinate_value)
            table.append(row)
                
        
        return table
#     [
#                ['Year', 'Austria', 'Belgium', 'Czech Republic', 'Finland', 'France', 'Germany'],
#                ['2003', 1336060, 3817614, 974066, 1104797, 6651824, 15727003],
#                ['2004', 1538156, 3968305, 928875, 1151983, 5940129, 17356071],
#                ['2005', 1576579, 4063225, 1063414, 1156441, 5714009, 16716049],
#                ['2006', 1600652, 4604684, 940478, 1167979, 6190532, 18542843],
#                ['2007', 1968113, 4013653, 1037079, 1207029, 6420270, 19564053],
#                ['2008', 1901067, 6792087, 1037327, 1284795, 6240921, 19830493]
#                             ]
        

