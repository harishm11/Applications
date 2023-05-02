from django.contrib import admin
from django.urls import path
from productconfigurator import views


urlpatterns = [

    path('productpage', views.productpage, name="productpage")

]
