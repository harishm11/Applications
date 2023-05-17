from django.db import models
from ..models.carrier import Carrier


class Uwcompany(models.Model):
    CompanyName = models.CharField(max_length=255, null=True, blank=True)
    Carrier = models.ForeignKey(
        Carrier, on_delete=models.CASCADE, null=True, blank=True)
    EnableInd = models.BooleanField(default=True)

    def __str__(self):
        return self.CompanyName
