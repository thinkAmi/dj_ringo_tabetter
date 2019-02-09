from apps.highcharts import views
from django.urls import path

app_name = 'highcharts'

urlpatterns = [
    path('total', views.total, name='total'),
    path('total-by-month', views.total_by_month, name='total_by_month'),
]
