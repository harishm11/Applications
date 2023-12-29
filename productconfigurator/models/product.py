from django import forms
from django.db import models
from django.apps import apps
from systemtables.models.coverage import Coverage
# from systemtables.models.discount import Discount
# from systemtables.models.surcharge import Surcharge

from systemtables.models.state import State
from systemtables.models.carrier import Carrier
from systemtables.models.uwcompany import Uwcompany
from systemtables.models.offering import Offering
from systemtables.models.policytype import PolicyType
from systemtables.models.policysubtype import PolicySubType
from systemtables.models.policyterm import PolicyTerm
from systemtables.models.lineofbusiness import LineOfBusiness
from systemtables.models.productcode import ProductCode
from systemtables.models.coverage import Coverage
from systemtables.models.coverageoptions import CoverageOptions


class Product(models.Model):

    StateCode = models.ForeignKey(State, on_delete=models.CASCADE)
    Carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    UwCompany = models.ForeignKey(Uwcompany, on_delete=models.CASCADE)
    LineOfBusiness = models.ForeignKey(
        LineOfBusiness, on_delete=models.CASCADE)
    PolicyType = models.ForeignKey(PolicyType, on_delete=models.CASCADE)
    PolicySubType = models.ForeignKey(PolicySubType, on_delete=models.CASCADE)
    Policyterm = models.ForeignKey(PolicyTerm, on_delete=models.CASCADE)
    ProductCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE)
    Offering = models.ForeignKey(Offering, on_delete=models.CASCADE)
    EffectiveDate = models.DateField(null=True, blank=True)
    ExpiryDate = models.DateField(null=True, blank=True)
    # OpenBookInd = models.BooleanField(null=True, blank=True, default=True)
    # OpenBookStartDate = models.DateField(null=True, blank=True)
    # CloseBookEndDate = models.DateField(null=True, blank=True)
    CreateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    UpdateTime = models.DateTimeField(auto_now=True, blank=True, null=True)
    # coverages = models.ManyToManyField(Coverage, through='ProductCoverage')

    class Meta:
        unique_together = ('StateCode', 'Carrier', 'UwCompany',
                           'LineOfBusiness', 'PolicyType', 'PolicySubType', 'Policyterm')

    def __str__(self):
        return f"{self.StateCode} {self.Carrier} {self.UwCompany} {self.LineOfBusiness} {self.PolicyType} {self.PolicySubType}"


class ProductCoverage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    CoverageName = models.ForeignKey(Coverage, on_delete=models.CASCADE)
    # options = models.ManyToManyField(
    #     CoverageOptions, through='ProductCoverageOption')
    EffectiveDate = models.DateField(null=True, blank=True)
    ExpiryDate = models.DateField(null=True, blank=True)
    CreateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    UpdateTime = models.DateTimeField(auto_now=True, blank=True, null=True)


class ProductCoverageOption(models.Model):
    ProductCoverage = models.ForeignKey(
        ProductCoverage, on_delete=models.CASCADE)
    OptionValue = models.ForeignKey(CoverageOptions, on_delete=models.CASCADE)
    EffectiveDate = models.DateField(null=True, blank=True)
    ExpiryDate = models.DateField(null=True, blank=True)
    CreateTime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    UpdateTime = models.DateTimeField(auto_now=True, blank=True, null=True)
