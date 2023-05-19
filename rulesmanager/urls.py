# from django.contrib import admin
from django.urls import path
from rulesmanager import views


urlpatterns = [
    path('', views.rulesmanager,
         name='rulesmanager'),
    #     path('createrule/', views.createRule,
    #          name='createrule'),

]
