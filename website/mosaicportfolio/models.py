from django.db import models
from django.contrib.auth.models import User

class SiteKind:
    github = 1
    values = [(github, "github")]       

class RepositoryKind:
    git = 1
    values = [(git, "git")]

class WikiKind:
    github = 1
    values = [(github, "github")]

class IssueTrackerKind:
    github = 1
    values = [(github, "github")]

class Repository(models.Model):
    url = models.CharField(max_length=200)
    kind = models.IntegerField(choices=RepositoryKind.values)

    class Meta:
        verbose_name_plural = "repositories"

    def __str__(self):
        return "%s(%s)" % (self.url, self.kind)
    
    def __str__(self):
        return "%s" % self.url
    
class Wiki(models.Model):
    url = models.CharField(max_length=200)
    kind = models.IntegerField(choices=WikiKind.values)

    def __str__(self):
        return "%s(%s)" % (self.url, self.kind)
    
class IssueTracker(models.Model):
    url = models.CharField(max_length=200)
    kind = models.IntegerField(choices=IssueTrackerKind.values)

    def __str__(self):
        return "%s(%s)" % (self.url, self.kind)

class UserSite(models.Model):
    user = models.ForeignKey(User)
    login = models.CharField(max_length=200)
    kind = models.IntegerField(choices=SiteKind.values)

    def __str__(self):
        return "%s: %s@%s" % (self.user, self.login, self.kind)
    
class Project(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return "%s@%s" % (self.user, self.name)
     
class ProjectRepository(models.Model):
    project = models.ForeignKey(Project)
    login = models.CharField(max_length=200)
    repository = models.ForeignKey(Repository)

    class Meta:
        verbose_name_plural = "project repositories"

    def __str__(self):
        return "%s@%s" % (self.login, self.repository) 

class ProjectWiki(models.Model):
    project = models.ForeignKey(Project)
    login = models.CharField(max_length=200)
    wiki = models.ForeignKey(Wiki)

    def __str__(self):
        return "%s@%s" % (self.login, self.wiki) 

class ProjectIssueTracker(models.Model):
    project = models.ForeignKey(Project)
    login = models.CharField(max_length=200)
    issue_tracker = models.ForeignKey(IssueTracker)

    def __str__(self):
        return "%s@%s" % (self.login, self.issue_tracker)
     
class Activity(models.Model):
    date = models.DateTimeField()
    login = models.CharField(max_length=200)

    class Meta:
        abstract = True
        verbose_name_plural = "activities"
         
class RepositoryActivity(Activity):
    repository = models.ForeignKey(Repository)

    class Meta:
        verbose_name_plural = "repository activities"

    def __str__(self):
        return "%s@%s(%s)" % (self.login, self.repository, self.date)

class IssueTrackerActivity(Activity):
    issue_tracker = models.ForeignKey(IssueTracker)

    class Meta:
        verbose_name_plural = "issue tracker activities"

    def __str__(self):
        return "%s@%s(%s)" % (self.login, self.issue_tracker, self.date)

class WikiActivity(Activity):
    wiki = models.ForeignKey(Wiki)

    class Meta:
        verbose_name_plural = "wiki activities"

    def __str__(self):
        return "%s@%s(%s)" % (self.login, self.wiki, self.date)

