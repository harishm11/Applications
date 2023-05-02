from django.contrib import admin
from .models.validvaluetables.state import *
from .models.validvaluetables.carrier import *
from .models.configtables.product import *
from .models import *


admin.site.register(Productmodel)
admin.site.register(Statemodel)
admin.site.register(Carriermodel)
