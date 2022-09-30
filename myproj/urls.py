
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp1/',include('myapp1.urls')),
    path('',include('myapp2.urls')),
    path('myapp3/',include('myapp3.urls')),
    path('accounts/', include('django.contrib.auth.urls')),


]
