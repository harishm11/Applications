from django.db import models
from systemtables.models import \
    state, carrier, lineofbusiness, \
    uwcompany, productcode, policytype, policysubtype
from django.contrib.postgres.fields import ArrayField


class RatebookMetadata(models.Model):
    RatebookID = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        default=None
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
    LineofBusiness = models.ForeignKey(
        lineofbusiness.LineOfBusiness,
        on_delete=models.CASCADE,
        default=None
        )
    UWCompany = models.ForeignKey(
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
        blank=True,
        null=False,
        default=None
        )
    RatebookVersion = models.FloatField(
        null=False,
        default=None
        )
    RatebookName = models.CharField(
        max_length=100,
        null=False,
        default=None
        )
    RatebookRevisionType = models.CharField(
        max_length=50,
        null=False,
        default=None
        )
    RatebookStatusType = models.CharField(
        max_length=50,
        null=False,
        default=None
        )
    RatebookChangeType = models.CharField(
        max_length=50,
        null=False,
        default=None
        )
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

    def save(self, *args, **kwargs):
        self.RatebookName = str(self.State) + '_' + str(self.ProductCode)
        super(RatebookMetadata, self).save(*args, **kwargs)


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
    TableCategory = models.CharField(max_length=100, null=False)
    Coverage = models.CharField(max_length=100, null=False)
    Exhibit = models.CharField(max_length=100, null=False)
    Factor = models.CharField(max_length=100, null=True)
    RatingVarName1 = models.CharField(max_length=100, null=True)
    RatingVarName2 = models.CharField(max_length=100, null=True)
    RatingVarValue1 = models.CharField(max_length=100, null=True)
    RatingVarValue2 = models.CharField(max_length=100, null=True)
    RatingVarName3 = models.CharField(max_length=100, null=True)
    RatingVarName4 = models.CharField(max_length=100, null=True)
    RatingVarValue3 = models.CharField(max_length=100, null=True)
    RatingVarValue4 = models.CharField(max_length=100, null=True)
    RatingVarName5 = models.CharField(max_length=100, null=True)
    RatingVarName6 = models.CharField(max_length=100, null=True)
    RatingVarValue5 = models.CharField(max_length=100, null=True)
    RatingVarValue6 = models.CharField(max_length=100, null=True)
    RatingVarName7 = models.CharField(max_length=100, null=True)
    RatingVarName8 = models.CharField(max_length=100, null=True)
    RatingVarValue7 = models.CharField(max_length=100, null=True)
    RatingVarValue8 = models.CharField(max_length=100, null=True)
    RatingVarName9 = models.CharField(max_length=100, null=True)
    RatingVarName10 = models.CharField(max_length=100, null=True)
    RatingVarValue9 = models.CharField(max_length=100, null=True)
    RatingVarValue10 = models.CharField(max_length=100, null=True)
    RatingVarName11 = models.CharField(max_length=100, null=True)
    RatingVarName12 = models.CharField(max_length=100, null=True)
    RatingVarValue11 = models.CharField(max_length=100, null=True)
    RatingVarValue12 = models.CharField(max_length=100, null=True)
    RatingVarName13 = models.CharField(max_length=100, null=True)
    RatingVarName14 = models.CharField(max_length=100, null=True)
    RatingVarValue13 = models.CharField(max_length=100, null=True)
    RatingVarValue14 = models.CharField(max_length=100, null=True)
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


class RatingExhibits(models.Model):
    Ratebook = models.ForeignKey(
        RatebookMetadata,
        on_delete=models.CASCADE
    )
    RatingItemCode = models.CharField(max_length=100, null=True)
    Exhibit = models.CharField(max_length=100, null=True)
    Coverages = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    RatingVarNames = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    TableDescription = models.CharField(max_length=100, null=True)
    Version = models.FloatField(max_length=100, null=True)


class RatingVariables(models.Model):
    Exhibit = models.ForeignKey(
        RatingExhibits,
        on_delete=models.CASCADE
        )
    RatingVarName = models.CharField(max_length=200, null=True, blank=True)
    DisplayName = models.CharField(max_length=200)
    RatingVarType = models.CharField(max_length=200)
    RatingVarLength = models.CharField(max_length=200)
    RatingVarFormat = models.CharField(max_length=200)
    RateVarCategory = models.CharField(max_length=200)
