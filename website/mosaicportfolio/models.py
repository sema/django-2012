from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class SiteKind:
    github = "github"
    values = [("github", "github")]

class RepositoryKind:
    git = "git"
    values = [("git", "git")]

class WikiKind:
    github = "github"
    values = [("github", "github")]

class IssueTrackerKind:
    github = "github"
    values = [("github", "github")]

class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile')

    tag_line = models.CharField(max_length=256, blank=True)

def create_user_profile(**kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_user_profile, sender=User)

class UserSite(models.Model):
    user = models.ForeignKey(User)
    login = models.CharField(max_length=200)
    concrete_type = models.CharField(max_length=16, choices=SiteKind.values)

    def __str__(self):
        return "%s: %s@%s" % (self.user, self.login, self.concrete_type)

class Project(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return "%s@%s" % (self.user, self.name)

class Repository(models.Model):
    projects = models.ManyToManyField(Project, through='ProjectRepository')

    url = models.CharField(max_length=200)
    concrete_type = models.CharField(max_length=16, choices=RepositoryKind.values)
    last_updated = models.DateTimeField()

    class Meta:
        verbose_name_plural = "repositories"
        unique_together = [('concrete_type', 'url')]

    def save(self, *args, **kwargs):
        """
        Enforce a default last_updated timestamp sometime in the faraway past,
        makes it much more simple for us to get a prioritized list of repositories
        for processing on the back-ends.
        """

        if self.last_updated is None:
            self.last_updated = datetime.fromtimestamp(0)

        return super(Repository, self).save(*args, **kwargs)

    def __str__(self):
        return "%s(%s)" % (self.url, self.concrete_type)


class ProjectRepository(models.Model):
    project = models.ForeignKey(Project)
    repository = models.ForeignKey(Repository)

    login = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "project repositories"

    def __str__(self):
        return "%s@%s" % (self.login, self.repository)

class Wiki(models.Model):
    projects = models.ManyToManyField(Project, through='ProjectWiki')

    url = models.CharField(max_length=200)
    concrete_type = models.CharField(max_length=16, choices=WikiKind.values)

    def __str__(self):
        return "%s(%s)" % (self.url, self.concrete_type)

class ProjectWiki(models.Model):
    project = models.ForeignKey(Project)
    wiki = models.ForeignKey(Wiki)

    login = models.CharField(max_length=200)

    def __str__(self):
        return "%s@%s" % (self.login, self.wiki)

class IssueTracker(models.Model):
    projects = models.ManyToManyField(Project, through='ProjectIssueTracker')

    url = models.CharField(max_length=200)
    concrete_type = models.CharField(max_length=16, choices=IssueTrackerKind.values)

    def __str__(self):
        return "%s(%s)" % (self.url, self.concrete_type)

class ProjectIssueTracker(models.Model):
    project = models.ForeignKey(Project)
    issue_tracker = models.ForeignKey(IssueTracker)

    login = models.CharField(max_length=200)

    def __str__(self):
        return "%s@%s" % (self.login, self.issue_tracker)
     
class Activity(models.Model):
    date = models.DateTimeField()
    login = models.CharField(max_length=200)

    class Meta:
        abstract = True
         
class RepositoryActivity(Activity):
    repository = models.ForeignKey(Repository, related_name='activities')

    class Meta:
        verbose_name_plural = "repository activities"
        get_latest_by = 'date'

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

