from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('dashboard', views.open_dashboard, name='dashboard'),
    path('newssearch', views.newssearch_page, name='newssearch'),
    path('newsdashboard', views.open_news_dashboard, name='newsdashboard'),
]
