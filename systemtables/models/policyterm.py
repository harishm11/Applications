from django.db import models
from ..models.lineofbusiness import LineOfBusiness


class PolicyTerm(models.Model):
    PolicyTerm = models.CharField(max_length=100)
    Lob = models.ForeignKey(
        LineOfBusiness, on_delete=models.CASCADE, null=True, blank=True)
    EnableInd = models.BooleanField(default=True)

    def __str__(self):
        return self.PolicyTerm
