from django.db import models


class carrier(models.Model):
    CarrierName = models.CharField(max_length=100)
    NAICCode = models.CharField(max_length=10)
    FullCompanyName = models.CharField(max_length=200)
    AmbestNumber = models.CharField(max_length=10)

    def __str__(self):
        return self.CarrierName
