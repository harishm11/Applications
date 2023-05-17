from django.db import models


class Surcharge(models.Model):
    SurchargeName = models.CharField(max_length=50)
    SurchargeCode = models.CharField(max_length=50)
    SurchargeDesc = models.CharField(max_length=100)
    RatingItemCode = models.CharField(max_length=10)
    EnableInd = models.BooleanField(default=True)

    def __str__(self):
        return self.SurchargeName
