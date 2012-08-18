from django.conf.urls import patterns, include, url

urlpatterns = patterns('mosaicportfolio.views',
    url(r'^editprofile/', 'profile_edit', name='profile_edit'),
    url(r'^portfolio/(?P<username>\w+)/', 'portfolio', name='portfolio'),
    url(r'^$', 'home', name='home')
)
