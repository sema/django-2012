class SimpleActivity(object):
    '''
    Simple wrapper object for a commit.
    '''
    def __init__(self, date, login):
        self.date = date
        self.login = login
        
    def __str__(self):
        return "%s: '%s'" % (self.date, self.login)
