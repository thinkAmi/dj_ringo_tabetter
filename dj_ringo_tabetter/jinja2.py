from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment


# Djangoのtemplatetagsを利用できるように設定
# https://docs.djangoproject.com/en/2.1/topics/templates/#django.template.backends.jinja2.Jinja2
def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    return env
