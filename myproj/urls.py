
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authenticate.urls')),
    path('ratemanager/', include('ratemanager.urls')),
    path('rulesmanager/', include('rulesmanager.urls')),
    path('productconfigurator/', include('productconfigurator.urls')),
    path('systemtables/', include('systemtables.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('datatable/', include('datatable.urls')),

]
