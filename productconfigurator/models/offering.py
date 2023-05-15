from django.db import models


class Offering(models.Model):
    OfferingName = models.CharField(max_length=255, null=True, blank=True)
    EnableInd = models.BooleanField(default=True)

    def __str__(self):
        return self.OfferingName
