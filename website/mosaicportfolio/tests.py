import simplejson

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Repository

class APITest(TestCase):
    def test_get_worklist_item(self):

        # get the oldest element, repository 1

        response = self.client.get(reverse('api_worklist', kwargs={'type': 'repository'}))
        self.assertEqual(200, response.status_code)

        json = simplejson.loads(response.content)
        self.assertEqual(1, len(json))

        item = json[0]
        self.assertEqual('http://repository1', item['url'])
        self.assertEqual('2012-08-18T01:56:54+00:00', item['since'])

        # now update repository 1 and see if we get the now "older" repository 2

        repository = Repository.objects.get(pk=1)
        repository.last_updated = timezone.now()
        repository.save()

        response = self.client.get(reverse('api_worklist', kwargs={'type': 'repository'}))
        self.assertEqual(200, response.status_code)

        json = simplejson.loads(response.content)
        self.assertEqual(1, len(json))

        item = json[0]
        self.assertEqual('http://repository2', item['url'])
        self.assertEqual(None, item['since'])

        # finally update repository 2, and ensure that we don't get any repositories because of the
        # 24 hour threshold

        repository = Repository.objects.get(pk=2)
        repository.last_updated = timezone.now()
        repository.save()

        response = self.client.get(reverse('api_worklist', kwargs={'type': 'repository'}))
        self.assertEqual(200, response.status_code)

        json = simplejson.loads(response.content)
        self.assertEqual(0, len(json))