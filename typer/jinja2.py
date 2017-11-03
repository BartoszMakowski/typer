from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.utils.timezone import template_localtime
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.filters.update({
        'localtime': template_localtime,
    })
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'localtime': template_localtime,
    })
    return env
