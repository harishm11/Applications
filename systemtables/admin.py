from django.contrib import admin

from .models.state import State
from .models.carrier import Carrier

from .models.uwcompany import Uwcompany
from .models.coverage import Coverage
from .models.lineofbusiness import LineOfBusiness
from .models.policysubtype import PolicySubType
from .models.policytype import PolicyType
from .models.policyterm import PolicyTerm
from .models.productcode import ProductCode
from .models.offering import Offering
from .models.discount import Discount
from .models.surcharge import Surcharge
from .models.ratingvariables import RatingVariable
from .models.ratingexhibits import RatingExhibit
from .models.coverageoptions import CoverageOptions

admin.site.register(State)
admin.site.register(Carrier)
admin.site.register(Coverage)
admin.site.register(CoverageOptions)
admin.site.register(Uwcompany)
admin.site.register(LineOfBusiness)
admin.site.register(PolicyType)
admin.site.register(PolicySubType)
admin.site.register(PolicyTerm)
admin.site.register(ProductCode)
admin.site.register(Offering)
admin.site.register(Discount)
admin.site.register(Surcharge)
admin.site.register(RatingVariable)
admin.site.register(RatingExhibit)
