from . import views
from django.contrib import admin
from django.urls import path
from .views import *
from django.urls import path


urlpatterns = [
    path('createModel/',
         views.createModel, name='createModel'),
    path('', views.systemtables,
         name='systemtables'),
]
