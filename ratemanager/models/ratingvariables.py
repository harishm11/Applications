from django.db import models


class RatingVariables(models.Model):
    RateVarCategory = models.CharField(null=True, max_length=200, default=None)
    RatingVarName = models.CharField(null=True, max_length=200, default=None)
    DisplayName = models.CharField(null=True, max_length=200, default=None)
    RatingVarType = models.CharField(null=True, max_length=200, default=None)
    RatingVarLength = models.CharField(null=True, max_length=200, default=None)
    RatingVarFormat = models.CharField(null=True, max_length=200, default=None)

    def __str__(self) -> str:
        return self.RatingVarName
