from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from mosaicportfolio.models import RepositoryActivity, Repository, \
    ProjectRepository
import logging
logger = logging.getLogger(__name__)
def make_user_graph(user):
    project_repositories = ProjectRepository.objects.filter(project__user=user)#.prefetch_related('repository__repositoryactivity')
    grouped_activities = {}
    for prep in project_repositories:
        grouped_activities[prep.project.name] = RepositoryActivity.objects.filter(repository=prep.repository).filter(login=prep.login)
    return Graph(_("Activity graph for %s") % user.email, TableData(grouped_activities)).to_dict()

def make_project_graph(project):
    return make_user_graph(project)

class Graph(object):
    def __init__(self, title, table):
        self.title = title
        self.table = table
    
    def to_dict(self):
        return {'title': self.title, 'vTitle': _("Activities"), 'hTitle': _('Time'), 'table': self.table.to_list()}
     
class TableData(object):
    def __init__(self, grouped_actitivies):
        self.grouped_actitivies = grouped_actitivies
    
    def to_list(self):
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
        

