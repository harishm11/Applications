from django.db import models
from ..models.policytype import PolicyType


class PolicySubType(models.Model):
    PolicySubTypeName = models.CharField(
        max_length=255, null=True, blank=True, unique=True, verbose_name='Policy Sub Type')
    PolicyType = models.ForeignKey(PolicyType, on_delete=models.CASCADE)
    EnableInd = models.BooleanField(default=True)

    class Meta:
        unique_together = ('PolicySubTypeName', 'PolicyType')

    def __str__(self):
        return self.PolicySubTypeName
