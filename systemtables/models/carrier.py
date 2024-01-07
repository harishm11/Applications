from django.db import models


class Carrier(models.Model):
    CarrierName = models.CharField(max_length=100, verbose_name="Carrier Name")
    NAICCode = models.CharField(max_length=10, verbose_name="NAIC Code")
    FullCompanyName = models.CharField(max_length=200, verbose_name="Full Company Name")
    AmbestNumber = models.CharField(max_length=10, verbose_name="Ambest Number")
    EnableInd = models.BooleanField(default=True)

    class Meta:
        unique_together = ('CarrierName', 'NAICCode', 'FullCompanyName',
                           'AmbestNumber')

    def __str__(self):
        return self.CarrierName
