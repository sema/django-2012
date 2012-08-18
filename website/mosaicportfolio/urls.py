from django.conf.urls import patterns, include, url

urlpatterns = patterns('mosaicportfolio.views',
    url(r'^api/worklist/(?P<abstract_type>\w+)/(?P<concrete_type>\w+)/deliver/', 'api_worklist_deliver', name='api_worklist_deliver'),
    url(r'^api/worklist/(?P<abstract_type>\w+)/(?P<concrete_type>\w+)/', 'api_worklist', name='api_worklist'),

    url(r'^editprofile/', 'profile_edit', name='profile_edit'),

    url(r'^portfolio/(?P<username>\w+)/', 'portfolio', name='portfolio'),
    url(r'^portfolio/', 'portfolio', name='portfolio'),

    url(r'^$', 'home', name='home')
)
