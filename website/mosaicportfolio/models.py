from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

class SiteKind:
    github = 1
    values = [(github, github)]
    
class UserSite(models.Model):
    user = models.ForeignKey(User)
    login = models.CharField(max_length=200)
    kind = models.IntegerField(choices=SiteKind.values)
    
class Project(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    description = models.TextField()

class ProjectRepository(models.Model):
    project = models.ForeignKey(Project)
    login = models.CharField(max_length=200)
    repository = models.ForeignKey(Repository)
    class Meta:
        verbose_name_plural = "project repositories"

class ProjectWiki(models.Model):
    project = models.ForeignKey(Project)
    login = models.CharField(max_length=200)
    wiki = models.ForeignKey(Wiki)

class ProjectIssueTracker(models.Model):
    project = models.ForeignKey(Project)
    login = models.CharField(max_length=200)
    issue_tracker = models.ForeignKey(IssueTracker)

class RepositoryKind:
    git = 1
    values = [(git, git)]
    
class Repository(models.Model):
    url = models.URLField()
    kind = models.IntegerField(choices=RepositoryKind.values)
    class Meta:
        verbose_name_plural = "repositories"

class WikiKind:
    github = 1
    values = [(github, github)]
    
class Wiki(models.Model):
    url = models.URLField()
    kind = models.IntegerField(choices=WikiKind.values)

class IssueTrackerKind:
    github = 1
    values = [(github, github)]
    
class IssueTracker(models.Model):
    url = models.URLField()
    kind = models.IntegerField(choices=IssueTrackerKind.values)

class Activity(models.Model):
    date = models.DateTimeField()
    login = models.CharField(max_length=200)
    class Meta:
        abstract = true
        verbose_name_plural = "activities"
        
class RepositoryActivity(Activity):
    repository = models.ForeignKey(Repository)
    class Meta:
        verbose_name_plural = "repository activities"

class IssueTrackerActivity(Activity):
    issue_tracker = models.ForeignKey(IssueTracker)
    class Meta:
        verbose_name_plural = "issue trakcer activities"

class WikiActivity(Activity):
    wiki = models.ForeignKey(Wiki)
    class Meta:
        verbose_name_plural = "wiki activities"

