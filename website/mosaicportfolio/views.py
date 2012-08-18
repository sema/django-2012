from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

def home(request):
    return render(request, "mosaicportfolio/home.html")

def portfolio(request, username=None):

    if username is None:
        if request.user.is_authenticated:
            return redirect(reverse('portfolio', kwargs={'username': request.user.username}))

    return render(request, "mosaicportfolio/portfolio.html")

def profile_edit(request):
    return render(request, "mosaicportfolio/profile_edit.html")