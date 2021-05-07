from django.urls import path
from django.conf.urls import url
from tweetApp import views

urlpatterns = [
    path('', views.home, name='home'),
]