from django.db import models
from ..models.productcode import ProductCode



class Coverage(models.Model):
    ProductCd = models.ForeignKey(
        ProductCode, on_delete=models.CASCADE, null=True, blank=True)
    CoverageName = models.CharField(max_length=100)
    CoverageCode = models.CharField(max_length=50)
    CoverageType = models.CharField(max_length=50)
    CoverageSequence = models.CharField(max_length=10)
    CoverageLevel = models.CharField(max_length=50)
    EnableInd = models.BooleanField(default=True)
    def __str__(self):
        return self.CoverageName

