from django.db import models
from ..models.productcode import ProductCode
from ..models.lineofbusiness import LineOfBusiness


class Coverage(models.Model):
    ProductCd = models.ForeignKey(
        ProductCode, on_delete=models.CASCADE, null=True, blank=True)
    CoverageName = models.CharField(max_length=100)
    CoverageLob = models.ForeignKey(
        LineOfBusiness, on_delete=models.CASCADE, null=True, blank=True)
    CoverageCode = models.CharField(max_length=50)
    CoverageType = models.CharField(max_length=50)
    CoverageSequence = models.CharField(max_length=10)
    CoverageLevel = models.CharField(max_length=50)
    EnableInd = models.BooleanField(default=True)

    class Meta:
        unique_together = ('ProductCd', 'CoverageName', 'CoverageLob',
                           'CoverageCode', 'CoverageType', 'CoverageSequence', 'CoverageLevel')

    def __str__(self):
        return self.CoverageName
