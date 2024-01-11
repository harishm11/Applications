from django.db import models
from ratemanager.models.ratebookmetadata import RatebookMetadata


class RatingFactors (models.Model):
    Ratebook = models.ForeignKey(
        RatebookMetadata,
        on_delete=models.CASCADE
    )
    RatebookID = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        default=None
    )
    RatebookVersion = models.FloatField(
        null=False,
        default=None
    )
    TableCategory = models.CharField(max_length=100, null=False, default=None)
    Coverage = models.CharField(max_length=100, null=False, default=None)
    Exhibit = models.CharField(max_length=100, null=False, default=None)
    Factor = models.CharField(max_length=100, null=True, default=None)
    RatingVarName1 = models.CharField(max_length=100, null=True, default=None)
    RatingVarName2 = models.CharField(max_length=100, null=True, default=None)
    RatingVarValue1 = models.CharField(max_length=100, null=True, default=None)
    RatingVarValue2 = models.CharField(max_length=100, null=True, default=None)
    RatingVarName3 = models.CharField(max_length=100, null=True, default=None)
    RatingVarName4 = models.CharField(max_length=100, null=True, default=None)
    RatingVarValue3 = models.CharField(max_length=100, null=True, default=None)
    RatingVarValue4 = models.CharField(max_length=100, null=True, default=None)
    RatingVarName5 = models.CharField(max_length=100, null=True, default=None)
    RatingVarName6 = models.CharField(max_length=100, null=True, default=None)
    RatingVarValue5 = models.CharField(max_length=100, null=True, default=None)
    RatingVarValue6 = models.CharField(max_length=100, null=True, default=None)
    RatingVarName7 = models.CharField(max_length=100, null=True, default=None)
    RatingVarName8 = models.CharField(max_length=100, null=True, default=None)
    RatingVarValue7 = models.CharField(max_length=100, null=True, default=None)
    RatingVarValue8 = models.CharField(max_length=100, null=True, default=None)

    NewBusinessEffectiveDate = models.DateField(
        null=False,
        default=None
    )
    NewBusinessExpiryDate = models.DateField(
        null=True,
        default=None
    )
    RenewalEffectiveDate = models.DateField(
        null=False,
        default=None
    )
    RenewalExpiryDate = models.DateField(
        null=True,
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
    CreationDateTime = models.DateTimeField(
        null=False,
        default=None
    )
    RecordStatus = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        default=None
    )
