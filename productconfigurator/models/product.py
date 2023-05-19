from django import forms
from django.db import models
from django.apps import apps
from systemtables.models.coverage import Coverage
from systemtables.models.discount import Discount
from systemtables.models.surcharge import Surcharge


class Product(models.Model):
    StateCode = models.CharField(max_length=2)
    Carrier = models.CharField(max_length=100)
    UwCompany = models.CharField(max_length=100)
    LineOfBusiness = models.CharField(max_length=20)
    PolicyType = models.CharField(max_length=100)
    PolicySubType = models.CharField(max_length=100)
    Policyterm = models.CharField(max_length=20)
    ProductCode = models.CharField(max_length=100)
    Offering = models.CharField(max_length=100)
    EffectiveDate = models.DateField(null=True, blank=True)
    ExpiryDate = models.DateField(null=True, blank=True)
    OpenBookInd = models.BooleanField(null=True, blank=True, default=True)
    OpenBookStartDate = models.DateField(null=True, blank=True)
    CloseBookEndDate = models.DateField(null=True, blank=True)
    CreateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    UpdateTime = models.DateTimeField(auto_now=True, blank=True, null=True)
    coverages = models.ManyToManyField(Coverage)
    discounts = models.ManyToManyField(Discount)
    surcharges = models.ManyToManyField(Surcharge)

    def __str__(self):
        return self.StateCode, self.Carrier, self.UwCompany, self.LineOfBusiness, self.PolicyType, self.PolicySubType



