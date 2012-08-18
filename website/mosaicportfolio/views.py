from datetime import timedelta
import simplejson

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed, HttpResponse, Http404, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import Repository, RepositoryActivity

def home(request):
    return render(request, "mosaicportfolio/home.html")

def portfolio(request, username=None):

    if username is None:
        if request.user.is_authenticated:
            return redirect(reverse('portfolio', kwargs={'username': request.user.username}))

    return render(request, "mosaicportfolio/portfolio.html")

def profile_edit(request):

    return render(request, "mosaicportfolio/profile_edit.html")

def api_worklist(request, abstract_type, concrete_type):
    """
    Returns a list of work items (as of now this list has only one item in it at a time)

    Each item is a dictionary {"url": <string>, "since": <string, date in iso-format>}

    Since indicates the latest item we have recorded for that particular repository, e.g. the
    worker should only look for items which are newer than this time.
    """
    threshold = timezone.now() - timedelta(days=1)

    items = []

    if abstract_type == 'repository':
        repositories = Repository.objects.all()\
                       .filter(concrete_type=concrete_type)\
                       .exclude(last_updated__gt=threshold)\
                       .order_by('last_updated')[:1]

        for repository in repositories:

            try:
                since = repository.activities.latest().date.isoformat()
            except RepositoryActivity.DoesNotExist:
                since = None

            items.append({'url': repository.url,
                          'since': since})

    else:
        return Http404()

    return HttpResponse(simplejson.dumps(items), content_type='application/json')

def api_worklist_deliver(request, abstract_type, concrete_type):
    """
    Accepts a delivery of activities for a single repository.

    A post request is accepted with the POST parameter "payload", which must be a
    JSON formatted dictionary with the following contents:

    {
        "url": <string, repository url>,
        "activities": [
            {
                "date": <string, iso formatted timestamp>,
                "login": <string, user identifier>
            } ...
        ]
    }

    """

    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    if abstract_type == 'repository':

        try:
            payload = simplejson.loads(request.POST['payload'])

            repository = get_object_or_404(Repository, url=payload['url'], concrete_type=concrete_type)

            for activity in payload['activities']:
                RepositoryActivity.objects.create(
                    repository=repository,
                    date=activity['date'],
                    login=activity['login']
                )

            return HttpResponse()

        except simplejson.JSONDecodeError:
            return HttpResponseBadRequest()

    else:
        return Http404()
