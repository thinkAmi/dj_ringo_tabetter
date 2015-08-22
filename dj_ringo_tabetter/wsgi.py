"""
WSGI config for dj_ringo_tabetter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_ringo_tabetter.settings")

application = get_wsgi_application()

# whitenoise用に追加
from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)
