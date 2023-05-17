from django.db import models


class Discount(models.Model):
    DiscountName = models.CharField(max_length=50)
    DiscountCode = models.CharField(max_length=50)
    DiscountDesc = models.CharField(max_length=100)
    RatingItemCode = models.CharField(max_length=10)
    EnableInd = models.BooleanField(default=True)

    def __str__(self):
        return self.DiscountName
