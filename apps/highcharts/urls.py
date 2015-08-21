from django.conf.urls import patterns, url
from apps.highcharts import views

urlpatterns = patterns('',
                       url(r'^total$', views.total),
                       url(r'^total-by-month$', views.total_by_month),
                       )
