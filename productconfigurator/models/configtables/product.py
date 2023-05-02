from django.db import models


class Productmodel(models.Model):
    Carrier = models.CharField(max_length=100)
    UwCompany = models.CharField(max_length=100)
    LineOfBusiness = models.CharField(max_length=20)
    PolicyTypeCode = models.CharField(max_length=100)
    PolicySubTypeCode = models.CharField(max_length=100)
    ProductCode = models.CharField(max_length=100)
    Offering = models.CharField(max_length=100)
    StateCode = models.CharField(max_length=100)
    StartDate = models.DateField()
    EndDate = models.DateField()
    OpenBookInd = models.BooleanField()
    CloseBookInd = models.BooleanField()
    OpenBookStartDate = models.DateField(null=True, blank=True)
    CloseBookEndDate = models.DateField(null=True, blank=True)
    CreateDate = models.DateField(auto_now_add=True, blank=True, null=True)
    UpdateDate = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.Carrier, self.UwCompany, self.LineOfBusiness, self.PolicyType, self.PolicySubType
