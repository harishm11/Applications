from django.db import models
from systemtables.models import \
    state, carrier, lineofbusiness, \
    uwcompany, productcode, policytype, \
    policysubtype


def setForeignKeysVerboseNames(self):
    self.fields['LineofBusiness'].verbose_name = lineofbusiness.LineOfBusiness._meta.get_field(
        'LobName').verbose_name
    self.fields['State'].verbose_name = state.State._meta.get_field(
        'StateCode').verbose_name
    self.fields['Carrier'].verbose_name = carrier.Carrier._meta.get_field(
        'CarrierName').verbose_name
    self.fields['UWCompany'].verbose_name = uwcompany.Uwcompany._meta.get_field(
        'CompanyName').verbose_name
    self.fields['ProductCode'].verbose_name = productcode.ProductCode._meta.get_field(
        'ProductCd').verbose_name
    self.fields['PolicyType'].verbose_name = policytype.PolicyType._meta.get_field(
        'PolicyTypeName').verbose_name
    self.fields['PolicySubType'].verbose_name = policysubtype.PolicySubType._meta.get_field(
        'PolicySubTypeName').verbose_name


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
        default=None,
        verbose_name='ID'
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
        default=None,
        verbose_name='Project ID'
    )
    ProjectDescription = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        default=None,
        verbose_name='Project Description'
    )
    RatebookVersion = models.FloatField(
        null=False,
        default=None,
        verbose_name='Version'
    )
    RatebookName = models.CharField(
        max_length=100,
        null=False,
        default=None,
        verbose_name='Name'
    )
    RatebookRevisionType = models.CharField(
        max_length=50,
        null=False,
        default=None,
        verbose_name='Revision Type'
    )
    RatebookStatusType = models.CharField(
        max_length=50,
        null=False,
        default=None,
        verbose_name='Status Type'
    )
    RatebookChangeType = models.CharField(
        max_length=50,
        null=False,
        default=None,
        verbose_name='Change Type'
    )
    NewBusinessEffectiveDate = models.DateField(
        null=False,
        default=None,
        verbose_name='New Business Effective Date'
    )
    NewBusinessExpiryDate = models.DateField(
        null=True,
        default=None,
        verbose_name='New Business Expiry Date'
    )
    RenewalEffectiveDate = models.DateField(
        null=False,
        default=None,
        verbose_name='Renewal Effective Date'
    )
    RenewalExpiryDate = models.DateField(
        null=True,
        default=None,
        verbose_name='Renewal Expiry Date'
    )
    ActivationDate = models.DateField(
        null=True,
        default=None,
        verbose_name='Activation Date'
    )
    ActivationTime = models.TimeField(
        null=True,
        default=None,
        verbose_name='Activation Time'
    )
    MigrationDate = models.DateField(
        null=True,
        default=None,
        verbose_name='Migration Date'
    )
    MigrationTime = models.TimeField(
        null=True,
        default=None,
        verbose_name='Migration Time'
    )
    CreationDateTime = models.DateTimeField(
        null=False,
        default=None,
        verbose_name='Creation DateTime'
    )
    Environment = models.CharField(
        max_length=50,
        default='Rate Development',
        null=True,
        verbose_name='Environment'
    )
    isDeleted = models.BooleanField(
        null=True,
        default=False,
        verbose_name='Delete Status'
    )
    onHold = models.BooleanField(
        null=True,
        default=False,
        verbose_name='Hold Status'
    )
    retrofitReq = models.BooleanField(
        null=True,
        default=False,
        verbose_name='Retrofit Required?'
    )

    def save(self, *args, **kwargs):
        self.RatebookName = str(self.State) + '_' + str(self.ProductCode)
        self.id = self.RatebookID + '_' + str(self.RatebookVersion)
        # setForeignKeysVerboseNames(self)
        super(RatebookMetadata, self).save(*args, **kwargs)
