import simplejson

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Repository, RepositoryActivity

class APITest(TestCase):

    token = '?token=%s' % settings.MOSAIC_WORKER_PRIVATE_TOKEN

    def test_get_worklist_item(self):

        def request():
            response = self.client.get(reverse('api_worklist', kwargs={
                'abstract_type': 'repository',
                'concrete_type': 'git'
            }) + self.token)

            self.assertEqual(200, response.status_code)

            return simplejson.loads(response.content)


        # get the oldest element, repository 1

        json = request()
        self.assertEqual(1, len(json))

        item = json[0]
        self.assertEqual('http://repository1', item['url'])
        self.assertEqual('2012-08-18T01:56:54+00:00', item['since'])

        # now update repository 1 and see if we get the now "older" repository 2

        repository = Repository.objects.get(pk=1)
        repository.last_updated = timezone.now()
        repository.save()

        json = request()
        self.assertEqual(1, len(json))

        item = json[0]
        self.assertEqual('http://repository2', item['url'])
        self.assertEqual(None, item['since'])

        # finally update repository 2, and ensure that we don't get any repositories because of the
        # 24 hour threshold

        repository = Repository.objects.get(pk=2)
        repository.last_updated = timezone.now()
        repository.save()

        json = request()
        self.assertEqual(0, len(json))

    def test_deliver_activities_malformed(self):

        response = self.client.post(reverse('api_worklist_deliver', kwargs={
            'abstract_type': 'repository',
            'concrete_type': 'git'
        }) + self.token, data={
            'payload': ''
        })

        self.assertEqual(400, response.status_code)

    def test_deliver_empty_activities(self):

        response = self.client.post(reverse('api_worklist_deliver', kwargs={
            'abstract_type': 'repository',
            'concrete_type': 'git'
        }) + self.token, data={
            'payload': '{"url": "http://repository1", "activities": []}'
        })

        self.assertEqual(200, response.status_code)

    def test_deliver_activities(self):

        start_activity_count = RepositoryActivity.objects.count()

        login = 'testuser'
        date = timezone.now()

        response = self.client.post(reverse('api_worklist_deliver', kwargs={
            'abstract_type': 'repository',
            'concrete_type': 'git'
        }) + self.token, data={
            'payload': '{"url": "http://repository1", "activities": [{"login": "%s", "date": "%s"}]}' % (login, date)
        })

        self.assertEqual(200, response.status_code)
        self.assertEqual(start_activity_count+1, RepositoryActivity.objects.count())