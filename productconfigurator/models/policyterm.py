from django.db import models


class PolicyTerm(models.Model):
    PolicyTerm = models.CharField(max_length=100)
    EnableInd = models.BooleanField(default=True)

    def __str__(self):
        return self.PolicyTerm
