from django.db import models
from systemtables.models import \
    state, carrier, lineofbusiness, \
    uwcompany, productcode, policytype, policysubtype


class RatebookGroups (models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False,
        auto_created=True
        )
    Carrier = models.ForeignKey(
        carrier.Carrier,
        on_delete=models.CASCADE
        )
    State = models.ForeignKey(
        state.State,
        on_delete=models.CASCADE
        )
    LoBusiness = models.ForeignKey(
        lineofbusiness.LineOfBusiness,
        on_delete=models.CASCADE
        )
    UwCompany = models.ForeignKey(
        uwcompany.Uwcompany,
        on_delete=models.CASCADE
        )
    PolicyType = models.ForeignKey(
        policytype.PolicyType,
        on_delete=models.CASCADE
        )
    PolicySubType = models.ForeignKey(
        policysubtype.PolicySubType,
        on_delete=models.CASCADE
        )
    ProductName = models.ForeignKey(
        productcode.ProductCode,
        on_delete=models.CASCADE
        )
    ProjectID = models.CharField(
        max_length=50,
        null=True,
        blank=True
        )
    NewBusinessEffectiveDate = models.DateTimeField(null=False)
    NewBusinessExpiryDate = models.DateTimeField(null=False)
    RenewalEffectiveDate = models.DateTimeField(null=False)
    RenewalExpiryDate = models.DateTimeField(null=False)
    ActivationDate = models.DateTimeField(null=False)
    ActivationTime = models.DateTimeField(null=False)

    def __str__(self):
        return str(self.id)


class RateBooks (models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False,
        auto_created=True
        )
    RatebookGroup = models.ForeignKey(
        RatebookGroups,
        on_delete=models.CASCADE
        )
    RatebookVersion = models.IntegerField(null=False)
    RatebookRevisionType = models.CharField(max_length=10, null=False)
    RatebookStatusType = models.CharField(max_length=10, null=False)
    RatebookChangeType = models.CharField(max_length=10, null=False)

    def __str__(self):
        return str(self.id)


class AllExhibits (models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False,
        auto_created=True
        )
    Ratebook = models.ForeignKey(
        RateBooks,
        on_delete=models.CASCADE
    )
    Coverage = models.CharField(max_length=100, null=False)
    Exhibit = models.CharField(max_length=100, null=False)
    Factor = models.CharField(max_length=100, null=False)
    RatingVarName1 = models.CharField(max_length=100, null=True)
    RatingVarName2 = models.CharField(max_length=100, null=True)
    RatingVarValue1 = models.CharField(max_length=100, null=True)
    RatingVarValue2 = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.Exhibit
