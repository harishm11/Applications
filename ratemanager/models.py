from django.db import models
from systemtables.models import \
    state, carrier, lineofbusiness, \
    uwcompany, productcode, policytype, policysubtype


class Ratebooks(models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False,
        auto_created=True
        )
    Carrier = models.ForeignKey(
        carrier.Carrier,
        on_delete=models.CASCADE,
        default=None
        )
    State = models.ForeignKey(
        state.State,
        on_delete=models.CASCADE,
        default=None
        )
    LoBusiness = models.ForeignKey(
        lineofbusiness.LineOfBusiness,
        on_delete=models.CASCADE,
        default=None
        )
    UwCompany = models.ForeignKey(
        uwcompany.Uwcompany,
        on_delete=models.CASCADE,
        default=None
        )
    PolicyType = models.ForeignKey(
        policytype.PolicyType,
        on_delete=models.CASCADE,
        default=None
        )
    PolicySubType = models.ForeignKey(
        policysubtype.PolicySubType,
        on_delete=models.CASCADE,
        default=None
        )
    ProductCode = models.ForeignKey(
        productcode.ProductCode,
        on_delete=models.CASCADE,
        default=None
        )
    ProjectID = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default=None
        )
    RatebookVersion = models.FloatField(
        null=False,
        default=None
        )
    RatebookRevisionType = models.CharField(
        max_length=10,
        null=False,
        default=None
        )
    RatebookStatusType = models.CharField(
        max_length=10,
        null=False,
        default=None
        )
    RatebookChangeType = models.CharField(
        max_length=10,
        null=False,
        default=None
        )
    NewBusinessEffectiveDate = models.DateField(
        null=False,
        default=None
        )
    NewBusinessExpiryDate = models.DateField(
        null=False,
        default=None
        )
    RenewalEffectiveDate = models.DateField(
        null=False,
        default=None
        )
    RenewalExpiryDate = models.DateField(
        null=False,
        default=None
        )
    ActivationDate = models.DateField(
        null=False,
        default=None
        )
    ActivationTime = models.TimeField(
        null=False,
        default=None
        )
    MigrationDate = models.DateField(
        null=False,
        default=None
        )
    MigrationTime = models.TimeField(
        null=False,
        default=None
        )


class AllExhibits (models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False,
        auto_created=True
        )
    Ratebook = models.ForeignKey(
        Ratebooks,
        on_delete=models.CASCADE
        )
    Coverage = models.CharField(max_length=100, null=False)
    Exhibit = models.CharField(max_length=100, null=False)
    Factor = models.CharField(max_length=100, null=False)
    RatingVarName1 = models.CharField(max_length=100, null=True)
    RatingVarName2 = models.CharField(max_length=100, null=True)
    RatingVarValue1 = models.CharField(max_length=100, null=True)
    RatingVarValue2 = models.CharField(max_length=100, null=True)
