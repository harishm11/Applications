from django.db import models
from ..models.lineofbusiness import LineOfBusiness


class PolicyType(models.Model):
    PolicyTypeName = models.CharField(max_length=255, null=True, blank=True, verbose_name='Policy Type')
    Lob = models.ForeignKey(
        LineOfBusiness, on_delete=models.CASCADE, null=True, blank=True)
    EnableInd = models.BooleanField(default=True)

    class Meta:
        unique_together = ('PolicyTypeName', 'Lob',)

    def __str__(self):
        return self.PolicyTypeName
