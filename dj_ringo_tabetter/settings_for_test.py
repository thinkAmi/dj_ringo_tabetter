from dj_ringo_tabetter.settings import *

# whitenoise向けの設定はデフォルトに戻さないと、以下のエラーが発生する
# ValueError: The file 'js/total_by_month.js' could not be found with
# <whitenoise.django.GzipManifestStaticFilesStorage object at 0x112daa908>.
STATICFILES_STORAGE = ''
