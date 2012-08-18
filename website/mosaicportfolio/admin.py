from django.contrib import admin
import models

admin.site.register(models.UserSite)
admin.site.register(models.Project)

admin.site.register(models.IssueTracker)
admin.site.register(models.IssueTrackerActivity)
admin.site.register(models.ProjectIssueTracker)

admin.site.register(models.Repository)
admin.site.register(models.ProjectRepository)
admin.site.register(models.RepositoryActivity)

admin.site.register(models.Wiki)
admin.site.register(models.WikiActivity)
admin.site.register(models.ProjectWiki)