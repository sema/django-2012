import os
import urlparse

from .settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
CRISPY_FAIL_SILENTLY = not DEBUG

ADMINS = (
 ('Casper S. Jensen', 'casper@svenningjensen.dk'),
 ('Esben Andreasen', 'esbenandreasen@gmail.com')
)

MANAGERS = ADMINS

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": {
                "postgres": "django.db.backends.postgresql_psycopg2"
            }[url.scheme],
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "media")
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "static")

MEDIA_URL = "/site_media/media/" # make sure this maps inside of site_media_url
STATIC_URL = "/site_media/static/" # make sure this maps inside of site_media_url
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

FILE_UPLOAD_PERMISSIONS = 0640

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
MOSAIC_WORKER_PRIVATE_TOKEN = os.environ.get('MOSAIC_WORKER_PRIVATE_TOKEN')

GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_API_SECRET = os.environ.get('GITHUB_API_SECRET')

GOOGLE_ANALYTICS = 'UA-300839-13'