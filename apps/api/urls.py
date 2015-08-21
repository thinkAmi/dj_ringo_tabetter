from django.conf.urls import patterns, url
from apps.api import views

urlpatterns = patterns('',
                       url(r'^v1/total/$', views.total_apples),
                       url(r'^v1/month/$', views.total_apples_by_month),
                       )