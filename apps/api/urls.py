from apps.api import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('v1/total/', views.TotalApplesView.as_view(), name='total'),
    path('v1/month/', views.TotalApplesByMonthView.as_view(), name='total_by_month'),
    path('v1/gather-tweets/', views.GatherTweetView.as_view(), name='gather_tweet'),
]
