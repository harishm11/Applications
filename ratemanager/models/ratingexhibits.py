from django.db import models


class RatingExhibits(models.Model):
    RatingItemCode = models.CharField(max_length=100, null=True, default=None)
    Exhibit = models.CharField(max_length=100, unique=True, default=None)
    DisplayName = models.CharField(null=True, max_length=200, default=None)
    Version = models.FloatField(max_length=100, null=True, default=None)
    SequenceNo = models.IntegerField(null=True, default=None)

    def __str__(self) -> str:
        return self.DisplayName
