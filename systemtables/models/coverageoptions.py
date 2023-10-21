from django.db import models
from .productcode import ProductCode
from django.apps import apps

Coverage = apps.get_model('systemtables', 'coverage')


class CoverageOption(models.Model):
    Coverage = models.ForeignKey(
        Coverage, on_delete=models.CASCADE)
    CoverageTerm = models.CharField(max_length=50)
    OptionValue = models.CharField(max_length=50)
    OptionDesc = models.CharField(max_length=200)
    Amount1 = models.CharField(max_length=50, null=True, blank=True)
    Amount2 = models.CharField(max_length=50, null=True, blank=True)
    Amount3 = models.CharField(max_length=50, null=True, blank=True)
    EnableInd = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Coverage.CoverageName} - {self.OptionValue}"

