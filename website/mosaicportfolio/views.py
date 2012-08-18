from django.shortcuts import render


def home(request):
    return render(request, "mosaicportfolio/home.html")

def portfolio(request, username):
    return render(request, "mosaicportfolio/portfolio.html")

def profile_edit(request):
    return render(request, "mosaicportfolio/profile_edit.html")