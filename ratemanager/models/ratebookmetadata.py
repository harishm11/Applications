from django.db import models
from systemtables.models import \
    state, carrier, lineofbusiness, \
    uwcompany, productcode, policytype, \
    policysubtype


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
