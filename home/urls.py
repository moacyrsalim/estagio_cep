from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home),
    url('api/zipcode', views.api),
    url('api/register_zipcode', views.register_zipcode),
]
