from django.db import models
from ..models.productcode import ProductCode
from ..models.lineofbusiness import LineOfBusiness


class Coverage(models.Model):
    ProductCd = models.ForeignKey(
        ProductCode, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Product Code")
    CoverageName = models.CharField(
        max_length=100, verbose_name="Coverage Name")
    CoverageLob = models.ForeignKey(
        LineOfBusiness, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Coverage LOB")
    CoverageCode = models.CharField(
        max_length=50, verbose_name="Coverage Code")
    CoverageType = models.CharField(
        max_length=50, verbose_name="Coverage Type")
    CoverageSequence = models.CharField(
        max_length=10, verbose_name="Coverage Sequence")
    CoverageLevel = models.CharField(
        max_length=50, verbose_name="Coverage Level")
    EnableInd = models.BooleanField(default=True)

    class Meta:
        unique_together = ('ProductCd', 'CoverageName', 'CoverageLob',
                           'CoverageCode', 'CoverageType', 'CoverageSequence', 'CoverageLevel')

    def __str__(self):
        return f"{self.CoverageName}"
