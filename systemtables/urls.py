from . import views
from django.contrib import admin
from django.urls import path
from .views import *
from django.urls import path


urlpatterns = [
    path('createsystemtable/',
         views.createModel, name='createsystemtable'),
    path('', views.systemtables,
         name='systemtables'),
    #     path('viewsystemtable/', views.viewsystemtable,
    #          name='viewsystemtable'),
]
