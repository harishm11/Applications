from . import views
from django.contrib import admin
from django.urls import path
from productconfigurator.views import views
from django.urls import path


urlpatterns = [
    path('create_model/', views.create_model, name='create_model'),
    path('', views.productconfigurator,
         name='productconfigurator'),
]
