from . import views
from django.contrib import admin
from django.urls import path
from productconfigurator.views import views
from django.urls import path


urlpatterns = [
    path('createModel/',
         views.createModel, name='createModel'),
    path('', views.productconfigurator,
         name='productconfigurator'),
]
