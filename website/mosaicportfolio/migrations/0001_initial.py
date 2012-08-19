# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('mosaicportfolio_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('tag_line', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mosaicportfolio', ['UserProfile'])

        # Adding model 'UserLink'
        db.create_table('mosaicportfolio_userlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('mosaicportfolio', ['UserLink'])

        # Adding model 'UserSite'
        db.create_table('mosaicportfolio_usersite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('concrete_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('mosaicportfolio', ['UserSite'])

        # Adding model 'Project'
        db.create_table('mosaicportfolio_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tag_line', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('mosaicportfolio', ['Project'])

        # Adding model 'Repository'
        db.create_table('mosaicportfolio_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('concrete_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('mosaicportfolio', ['Repository'])

        # Adding unique constraint on 'Repository', fields ['concrete_type', 'url']
        db.create_unique('mosaicportfolio_repository', ['concrete_type', 'url'])

        # Adding model 'ProjectRepository'
        db.create_table('mosaicportfolio_projectrepository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mosaicportfolio.Project'])),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mosaicportfolio.Repository'])),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('mosaicportfolio', ['ProjectRepository'])

        # Adding model 'Wiki'
        db.create_table('mosaicportfolio_wiki', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('concrete_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('mosaicportfolio', ['Wiki'])

        # Adding model 'ProjectWiki'
        db.create_table('mosaicportfolio_projectwiki', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mosaicportfolio.Project'])),
            ('wiki', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mosaicportfolio.Wiki'])),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('mosaicportfolio', ['ProjectWiki'])

        # Adding model 'IssueTracker'
        db.create_table('mosaicportfolio_issuetracker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('concrete_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('mosaicportfolio', ['IssueTracker'])

        # Adding model 'ProjectIssueTracker'
        db.create_table('mosaicportfolio_projectissuetracker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mosaicportfolio.Project'])),
            ('issue_tracker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mosaicportfolio.IssueTracker'])),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('mosaicportfolio', ['ProjectIssueTracker'])

        # Adding model 'RepositoryActivity'
        db.create_table('mosaicportfolio_repositoryactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activities', to=orm['mosaicportfolio.Repository'])),
        ))
        db.send_create_signal('mosaicportfolio', ['RepositoryActivity'])

        # Adding model 'IssueTrackerActivity'
        db.create_table('mosaicportfolio_issuetrackeractivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('issue_tracker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mosaicportfolio.IssueTracker'])),
        ))
        db.send_create_signal('mosaicportfolio', ['IssueTrackerActivity'])

        # Adding model 'WikiActivity'
        db.create_table('mosaicportfolio_wikiactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wiki', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mosaicportfolio.Wiki'])),
        ))
        db.send_create_signal('mosaicportfolio', ['WikiActivity'])


    def backwards(self, orm):
        # Removing unique constraint on 'Repository', fields ['concrete_type', 'url']
        db.delete_unique('mosaicportfolio_repository', ['concrete_type', 'url'])

        # Deleting model 'UserProfile'
        db.delete_table('mosaicportfolio_userprofile')

        # Deleting model 'UserLink'
        db.delete_table('mosaicportfolio_userlink')

        # Deleting model 'UserSite'
        db.delete_table('mosaicportfolio_usersite')

        # Deleting model 'Project'
        db.delete_table('mosaicportfolio_project')

        # Deleting model 'Repository'
        db.delete_table('mosaicportfolio_repository')

        # Deleting model 'ProjectRepository'
        db.delete_table('mosaicportfolio_projectrepository')

        # Deleting model 'Wiki'
        db.delete_table('mosaicportfolio_wiki')

        # Deleting model 'ProjectWiki'
        db.delete_table('mosaicportfolio_projectwiki')

        # Deleting model 'IssueTracker'
        db.delete_table('mosaicportfolio_issuetracker')

        # Deleting model 'ProjectIssueTracker'
        db.delete_table('mosaicportfolio_projectissuetracker')

        # Deleting model 'RepositoryActivity'
        db.delete_table('mosaicportfolio_repositoryactivity')

        # Deleting model 'IssueTrackerActivity'
        db.delete_table('mosaicportfolio_issuetrackeractivity')

        # Deleting model 'WikiActivity'
        db.delete_table('mosaicportfolio_wikiactivity')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mosaicportfolio.issuetracker': {
            'Meta': {'object_name': 'IssueTracker'},
            'concrete_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mosaicportfolio.Project']", 'through': "orm['mosaicportfolio.ProjectIssueTracker']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'mosaicportfolio.issuetrackeractivity': {
            'Meta': {'object_name': 'IssueTrackerActivity'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_tracker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mosaicportfolio.IssueTracker']"}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'mosaicportfolio.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tag_line': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['auth.User']"})
        },
        'mosaicportfolio.projectissuetracker': {
            'Meta': {'object_name': 'ProjectIssueTracker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_tracker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mosaicportfolio.IssueTracker']"}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mosaicportfolio.Project']"})
        },
        'mosaicportfolio.projectrepository': {
            'Meta': {'object_name': 'ProjectRepository'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mosaicportfolio.Project']"}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mosaicportfolio.Repository']"})
        },
        'mosaicportfolio.projectwiki': {
            'Meta': {'object_name': 'ProjectWiki'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mosaicportfolio.Project']"}),
            'wiki': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mosaicportfolio.Wiki']"})
        },
        'mosaicportfolio.repository': {
            'Meta': {'unique_together': "[('concrete_type', 'url')]", 'object_name': 'Repository'},
            'concrete_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'repositories'", 'symmetrical': 'False', 'through': "orm['mosaicportfolio.ProjectRepository']", 'to': "orm['mosaicportfolio.Project']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'mosaicportfolio.repositoryactivity': {
            'Meta': {'object_name': 'RepositoryActivity'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': "orm['mosaicportfolio.Repository']"})
        },
        'mosaicportfolio.userlink': {
            'Meta': {'object_name': 'UserLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['auth.User']"})
        },
        'mosaicportfolio.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_line': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'mosaicportfolio.usersite': {
            'Meta': {'object_name': 'UserSite'},
            'concrete_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mosaicportfolio.wiki': {
            'Meta': {'object_name': 'Wiki'},
            'concrete_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mosaicportfolio.Project']", 'through': "orm['mosaicportfolio.ProjectWiki']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'mosaicportfolio.wikiactivity': {
            'Meta': {'object_name': 'WikiActivity'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wiki': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mosaicportfolio.Wiki']"})
        }
    }

    complete_apps = ['mosaicportfolio']