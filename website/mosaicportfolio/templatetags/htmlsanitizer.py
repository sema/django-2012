import bleach

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@stringfilter
def sanitize_html(value):

    if isinstance(value, basestring):
        value = bleach.clean(value,
            tags=settings.HTML_SANITIZER_ALLOWED_TAGS,
            attributes=settings.HTML_SANITIZER_ALLOWED_ATTR,
            strip=True)

        return mark_safe(value)

    return value

register.filter('sanitize_html', sanitize_html)