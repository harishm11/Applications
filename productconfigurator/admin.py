from django.contrib import admin
from .models.validvaluetables.state import *
from .models.systemtables.product import *
from .models import *


admin.site.register(Productmodel)
admin.site.register(Statemodel)
