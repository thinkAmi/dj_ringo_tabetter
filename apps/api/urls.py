from apps.api import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('v1/total/', views.total_apples, name='total'),
    path('v1/month/', views.total_apples_by_month, name='total_by_month'),
]
