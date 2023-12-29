from django.db import models


class Carrier(models.Model):
    CarrierName = models.CharField(max_length=100)
    NAICCode = models.CharField(max_length=10)
    FullCompanyName = models.CharField(max_length=200)
    AmbestNumber = models.CharField(max_length=10)
    EnableInd = models.BooleanField(default=True)

    class Meta:
        unique_together = ('CarrierName', 'NAICCode', 'FullCompanyName',
                           'AmbestNumber')

    def __str__(self):
        return self.CarrierName
