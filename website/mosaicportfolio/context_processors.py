
from django.conf import settings

def google_analytics(request):

    return {'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', None)}