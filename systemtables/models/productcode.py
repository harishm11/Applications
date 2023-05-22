from django.db import models
from ..models.lineofbusiness import LineOfBusiness


class ProductCode(models.Model):
    ProductCd = models.CharField(max_length=10, null=True, blank=True)
    ProductName = models.CharField(max_length=255, null=True, blank=True)
    Lob = models.ForeignKey(
        LineOfBusiness, on_delete=models.CASCADE, null=True, blank=True)
    EnableInd = models.BooleanField(default=True)

    def __str__(self):
        return self.ProductCd
