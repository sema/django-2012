from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^register/$', 'registration.views.register',
            {'backend': 'registration.backends.simple.SimpleBackend'}, name='registration_register'),

    url(r'^', include('registration.auth_urls')),
    url(r'^', include('social_auth.urls')),

    url(r'^', include('mosaicportfolio.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
