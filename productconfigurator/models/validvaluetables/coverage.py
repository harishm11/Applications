from django.db import models


class Coverage(models.Model):
    CoverageName = models.CharField(max_length=100)
    CoverageCode = models.CharField(max_length=50)
    CoverageType = models.CharField(max_length=50)
    CoverageSequence = models.CharField(max_length=10)
    CoverageLevel = models.CharField(max_length=50)
    CoverageTerm = models.CharField(max_length=50)
    OptionValue = models.CharField(max_length=50)
    OptionDesc = models.CharField(max_length=200)
    Amount1 = models.CharField(max_length=50, null=True, blank=True)
    Amount2 = models.CharField(max_length=50, null=True, blank=True)
    Amount3 = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.CoverageName
