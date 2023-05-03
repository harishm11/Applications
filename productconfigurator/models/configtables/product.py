from django.db import models


class Productmodel(models.Model):
    StateCode = models.CharField(max_length=2)
    Carrier = models.CharField(max_length=100)
    UwCompany = models.CharField(max_length=100)
    LineOfBusiness = models.CharField(max_length=20)
    PolicyTypeCode = models.CharField(max_length=100)
    PolicySubTypeCode = models.CharField(max_length=100)
    Policyterms = models.CharField(max_length=20)
    ProductCode = models.CharField(max_length=100)
    Offering = models.CharField(max_length=100)
    EffectiveDate = models.DateField(null=True, blank=True)
    ExpiryDate = models.DateField(null=True, blank=True)
    OpenBookInd = models.BooleanField(null=True, blank=True)
    OpenBookStartDate = models.DateField(null=True, blank=True)
    CloseBookEndDate = models.DateField(null=True, blank=True)
    CreateDate = models.DateField(auto_now_add=True, blank=True, null=True)
    UpdateDate = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.StateCode, self.Carrier, self.UwCompany, self.LineOfBusiness, self.PolicyTypeCode, self.PolicySubTypeCode
