from datetime import timedelta, datetime
import time
import simplejson

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed, HttpResponse, Http404, HttpResponseBadRequest, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import  User

from .models import Repository, RepositoryActivity
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, "mosaicportfolio/home.html")

@login_required
def portfolio_redirect(request):
    return redirect(reverse('portfolio', kwargs={'username': request.user.username}))

def portfolio(request, username):
    user = get_object_or_404(User.objects.select_related(), username=username)

    isowner = request.user.is_authenticated() and request.user.username == user.username

    return render(request, "mosaicportfolio/portfolio.html", {
        'portfolio': user,
        'isowner': isowner
    })

@login_required()
def profile_edit(request):
    return render(request, "mosaicportfolio/profile_edit.html")

def api_worklist(request, abstract_type, concrete_type):
    """
    Returns a list of work items (as of now this list has only one item in it at a time)

    Each item is a dictionary {"url": <string>, "since": <string, unix timestamp>}

    Since indicates the latest item we have recorded for that particular repository, e.g. the
    worker should only look for items which are newer than this time.
    """

    if not request.GET.has_key('token') or request.GET.get('token') != settings.MOSAIC_WORKER_PRIVATE_TOKEN:
        return HttpResponseForbidden()

    threshold = timezone.now() - timedelta(days=1)

    items = []

    if abstract_type == 'repository':
        repositories = Repository.objects.all()\
                       .filter(concrete_type=concrete_type)\
                       .exclude(last_updated__gt=threshold)\
                       .order_by('last_updated')[:1]

        for repository in repositories:

            try:
                since = time.mktime(repository.activities.latest().date.timetuple())
            except RepositoryActivity.DoesNotExist:
                since = None

            items.append({'url': repository.url,
                          'since': since})

    else:
        return Http404()

    return HttpResponse(simplejson.dumps(items), content_type='application/json')

@csrf_exempt
def api_worklist_deliver(request, abstract_type, concrete_type):
    """
    Accepts a delivery of activities for a single repository.

    A post request is accepted with the POST parameter "payload", which must be a
    JSON formatted dictionary with the following contents:

    {
        "url": <string, repository url>,
        "activities": [
            {
                "date": <string, unix timestamp>,
                "login": <string, user identifier>
            } ...
        ]
    }

    """
    
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])
    
    if not request.GET.has_key('token') or request.GET.get('token') != settings.MOSAIC_WORKER_PRIVATE_TOKEN:
        return HttpResponseForbidden()
    
    if abstract_type == 'repository':

        try:
            payload = simplejson.loads(request.POST['payload'])

            repository = get_object_or_404(Repository, url=payload['url'], concrete_type=concrete_type)

            repository.last_updated = timezone.now()
            repository.save()

            for activity in payload['activities']:
                RepositoryActivity.objects.create(
                    repository=repository,
                    date=datetime.fromtimestamp(float(activity['date']), tz=timezone.get_current_timezone()),
                    login=activity['login']
                )
            return HttpResponse()

        except simplejson.JSONDecodeError as e:
            logger.execption(e)
            return HttpResponseBadRequest()
        logger.debug("POST5")
    else:
        return Http404()
