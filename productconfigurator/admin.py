from django.contrib import admin
from .models.validvaluetables.state import *
from .models.validvaluetables.carrier import *
from .models.configtables.product import *
from .models import *


admin.site.register(Product)
admin.site.register(state)
admin.site.register(carrier)
