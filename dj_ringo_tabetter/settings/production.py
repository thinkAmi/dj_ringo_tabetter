import os

from .base import *
import google.cloud.logging

DEBUG = False

# シークレットキーを上書き
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# staticファイルの設定
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = os.environ['GS_BUCKET_NAME']
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# 公開バケットを使用
GS_QUERYSTRING_AUTH = False
GS_DEFAULT_ACL = None

# ロギングの設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'cloud_logging': {
            'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
            'client': google.cloud.logging.Client(),
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['cloud_logging'],
            'level': 'INFO'
        },
    }
}
