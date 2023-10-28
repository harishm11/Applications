from django.db import models
from ..models.productcode import ProductCode


class Surcharge(models.Model):
    SurchargeName = models.CharField(max_length=50)
    SurchargeCode = models.CharField(max_length=50)
    SurchargeDesc = models.CharField(max_length=100)
    RatingItemCode = models.CharField(max_length=10)
    ProductCd = models.ForeignKey(
        ProductCode, on_delete=models.CASCADE, null=True, blank=True)
    EnableInd = models.BooleanField(default=True)

    class Meta:
        unique_together = ('SurchargeName', 'SurchargeCode', 'SurchargeDesc', 'RatingItemCode', 'ProductCd'
                           )

    def __str__(self):
        return self.SurchargeName
