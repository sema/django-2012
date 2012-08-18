from datetime import timedelta
import simplejson

from django.shortcuts import render, redirect, HttpResponse, Http404
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

def api_worklist(request, type):
    threshold = timezone.now() - timedelta(days=1)

    items = []

    if type == 'repository':
        repositories = Repository.objects.all()\
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

def api_worklist_deliver(request, type):
    pass


