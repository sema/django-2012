from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

from tastypie.api import Api
import registration.views

import forms
import api

v1_api = Api(api_name='v1')
v1_api.register(api.UserProfileResource())
v1_api.register(api.UserResource())
v1_api.register(api.UserGraphResource())
v1_api.register(api.ProjectGraphResource())
v1_api.register(api.EventResource())

urlpatterns = patterns('mosaicportfolio.views',
    url(r'^api/rest/', include(v1_api.urls)),

    url(r'^api/worklist/(?P<abstract_type>\w+)/(?P<concrete_type>\w+)/deliver/', 'api_worklist_deliver', name='api_worklist_deliver'),
    url(r'^api/worklist/(?P<abstract_type>\w+)/(?P<concrete_type>\w+)/', 'api_worklist', name='api_worklist'),

    url(r'^register/$', registration.views.register,
            {'backend': 'registration.backends.simple.SimpleBackend',
             'form_class': forms.RegistrationForm}, name='registration_register'),

    url(r'^login/$', auth_views.login,
            {'template_name': 'registration/login.html',
             'authentication_form': forms.AuthenticationForm}, name='auth_login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'registration/logout.html'}, name='auth_logout'),
    url(r'^password/change/$', auth_views.password_change, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='auth_password_reset_done'),

    url(r'^', include('social_auth.urls')),

    url(r'^editprofile/', 'profile_edit', name='profile_edit'),

    url(r'^portfolio/(?P<username>\w+)/', 'portfolio', name='portfolio'),
    url(r'^portfolio/', 'portfolio_redirect', name='portfolio'),

    url(r'^$', 'home', name='home')
)
