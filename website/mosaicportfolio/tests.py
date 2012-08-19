import simplejson

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Repository, RepositoryActivity
import graphing

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
        self.assertEqual('git://github.com/sema/HTTPdump.git', item['url'])
        self.assertEqual(1332761170.0, item['since'])

        # now update repository 1 and see if we get the now "older" repository 2

        repository = Repository.objects.get(pk=1)
        repository.last_updated = timezone.now()
        repository.save()

        json = request()
        self.assertEqual(1, len(json))

        item = json[0]
        self.assertEqual('git://github.com/sema/django-uni-form.git', item['url'])
        self.assertEqual(1279907567.0, item['since'])

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
            'payload': '{"url": "git://github.com/sema/HTTPdump.git", "activities": []}'
        })

        self.assertEqual(200, response.status_code)

    def test_deliver_activities(self):

        start_activity_count = RepositoryActivity.objects.count()

        login = 'testuser'
        date = '1345276614.0'

        response = self.client.post(reverse('api_worklist_deliver', kwargs={
            'abstract_type': 'repository',
            'concrete_type': 'git'
        }) + self.token, data={
            'payload': '{"url": "git://github.com/sema/django-2012.git", "activities": [{"login": "%s", "date": "%s"}]}' % (login, date)
        })

        self.assertEqual(200, response.status_code)
        self.assertEqual(start_activity_count + 1, RepositoryActivity.objects.count())

class UserLoginAndRegistrationTest(TestCase):

    def test_user_registration(self):

        response = self.client.post(reverse('registration_register'), data={
            'username': 'testuser1',
            'email': 'example@example.org',
            'password1': '1234',
            'password2': '1234'
        })
        self.assertEqual(302, response.status_code)

class TableDataTest(TestCase):
    def testEmpty(self):
        table = graphing.TableData({}).to_list()
        self.assertEquals([["Time"]], table)
    
    def testSingle(self):
        import datetime
        now = datetime.datetime.now()
        projectName = "P"
        
        repos = Repository.objects.all()
        activity = RepositoryActivity.objects.create(date=now, login="DrX", repository=repos[0])
        grouped = {}
        grouped[projectName] = [activity]
        table = graphing.TableData(grouped).to_list()
        self.assertEquals([["Time",                 projectName],
                           ["%s/%s" % (now.year, now.month), 1]], table)
    def testHorizontal(self):
        import datetime
        now = datetime.datetime.now()
        projectName1 = "P1"
        projectName2 = "P2"
        
        repos = Repository.objects.all()
        activity1 = RepositoryActivity.objects.create(date=now, login="DrX", repository=repos[0])
        activity2 = RepositoryActivity.objects.create(date=now, login="DrX", repository=repos[0])
        grouped = {}
        grouped[projectName1] = [activity1]
        grouped[projectName2] = [activity2]
        table = graphing.TableData(grouped).to_list()
        yearmonth = "%s/%s" % (now.year, now.month)
        self.assertEquals([["Time",  projectName1, projectName2],
                           [yearmonth, 1, 1]], table)
        
    def testAccumulate(self):
        import datetime
        now = datetime.datetime.now()
        projectName = "P"
        
        repos = Repository.objects.all()
        activity1 = RepositoryActivity.objects.create(date=now, login="DrX", repository=repos[0])
        activity2 = RepositoryActivity.objects.create(date=now, login="DrX", repository=repos[0])
        grouped = {}
        grouped[projectName] = [activity1, activity2]
        table = graphing.TableData(grouped).to_list()
        yearmonth = "%s/%s" % (now.year, now.month)
        self.assertEquals([["Time",  projectName],
                           [yearmonth, 2]], table)   
    def testVertical(self):
        import datetime
        now1 = datetime.datetime.now()
        now2 = datetime.datetime.fromtimestamp(0)
        projectName = "P"
        
        repos = Repository.objects.all()
        activity1 = RepositoryActivity.objects.create(date=now1, login="DrX", repository=repos[0])
        activity2 = RepositoryActivity.objects.create(date=now2, login="DrX", repository=repos[0])
        grouped = {}
        grouped[projectName] = [activity1, activity2]
        table = graphing.TableData(grouped).to_list()
        yearmonth1 = "%s/%s" % (now1.year, now1.month)
        yearmonth2 = "%s/%s" % (now2.year, now2.month)
        self.assertEquals([["Time",  projectName],
                           [yearmonth2, 1],
                           [yearmonth1, 1]
                           ], table) 
    def testDiagonal(self):
        import datetime
        now1 = datetime.datetime.now()
        now2 = datetime.datetime.fromtimestamp(0)
        projectName1 = "P1"
        projectName2 = "P2"
        
        repos = Repository.objects.all()
        activity1 = RepositoryActivity.objects.create(date=now1, login="DrX", repository=repos[0])
        activity2 = RepositoryActivity.objects.create(date=now2, login="DrX", repository=repos[0])
        grouped = {}
        grouped[projectName1] = [activity1]
        grouped[projectName2] = [activity2]
        table = graphing.TableData(grouped).to_list()
        yearmonth1 = "%s/%s" % (now1.year, now1.month)
        yearmonth2 = "%s/%s" % (now2.year, now2.month)
        self.assertEquals([["Time",  projectName1, projectName2],
                           [yearmonth2, 0, 1],
                           [yearmonth1, 1, 0]
                           ], table) 
