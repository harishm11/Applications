from django.db import models
from systemtables.models import \
    state, carrier, lineofbusiness, \
    uwcompany, productcode, policytype, policysubtype, coverage

# from django.apps import apps

# coverage = apps.get_model('systemtables', 'coverage')


class RatebookMetadata(models.Model):
    id = models.CharField(
        max_length=50,
        unique=True,
        default=None,
        null=False,
        primary_key=True,
        editable=False
    )
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
    ProjectDescription = models.CharField(
        max_length=500,
        blank=True,
        null=True,
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
    Environment = models.CharField(
        max_length=50,
        default='Rate Development',
        null=True
    )
    is_deleted = models.BooleanField(null=True, default=False)
    on_hold = models.BooleanField(null=True, default=False)

    def save(self, *args, **kwargs):
        self.RatebookName = str(self.State) + '_' + str(self.ProductCode)
        self.id = self.RatebookID + '_' + str(self.RatebookVersion)
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


# class RatingCoverages(models.Model):
#     CoverageCode = models.CharField(max_length=200, null=True, blank=True, default=None)
#     DisplayName = models.CharField(max_length=200, null=True, default=None)

#     def __str__(self) -> str:
#         return self.CoverageCode


class RatingExhibits(models.Model):
    RatingItemCode = models.CharField(max_length=100, null=True, default=None)
    Exhibit = models.CharField(max_length=100, unique=True, default=None)
    DisplayName = models.CharField(null=True, max_length=200, default=None)
    Version = models.FloatField(max_length=100, null=True, default=None)
    SequenceNo = models.IntegerField(null=True, default=None)

    def __str__(self) -> str:
        return self.Exhibit


class RatingVariables(models.Model):
    RateVarCategory = models.CharField(null=True, max_length=200, default=None)
    RatingVarName = models.CharField(null=True, max_length=200, default=None)
    DisplayName = models.CharField(null=True, max_length=200, default=None)
    RatingVarType = models.CharField(null=True, max_length=200, default=None)
    RatingVarLength = models.CharField(null=True, max_length=200, default=None)
    RatingVarFormat = models.CharField(null=True, max_length=200, default=None)

    def __str__(self) -> str:
        return self.RatingVarName


class RatebookTemplate(models.Model):
    RatebookID = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        default=None,
        editable=False
    )

    RatebookExhibit = models.ForeignKey(
        RatingExhibits, on_delete=models.DO_NOTHING)
    ExhibitVariables = models.ManyToManyField(RatingVariables)
    ExhibitCoverages = models.ManyToManyField(coverage.Coverage)
