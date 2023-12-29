from django.db import models
from ..models.productcode import ProductCode


class Discount(models.Model):
    DiscountName = models.CharField(max_length=50)
    DiscountCode = models.CharField(max_length=50)
    DiscountDesc = models.CharField(max_length=100)
    RatingItemCode = models.CharField(max_length=10)
    ProductCd = models.ForeignKey(
        ProductCode, on_delete=models.CASCADE, null=True, blank=True)
    EnableInd = models.BooleanField(default=True)

    class Meta:
        unique_together = ('DiscountName', 'DiscountCode', 'DiscountDesc',
                           'RatingItemCode', 'ProductCd')

    def __str__(self):
        return self.DiscountName
