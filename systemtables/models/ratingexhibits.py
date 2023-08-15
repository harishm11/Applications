from django.db import models


class RatingExhibit(models.Model):
    FACTOR_QUERY_METHOD_CHOICES = [
        ('Exact Match', 'Exact Match'),
        ('Range', 'Range'),
    ]

    RatingStepGroupCode = models.CharField(
        max_length=10, null=True, blank=True)
    RatingStepCode = models.CharField(max_length=10)
    ExhibitName = models.CharField(max_length=100)
    QueryMethod = models.CharField(
        max_length=50, choices=FACTOR_QUERY_METHOD_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.RatingItemGroup} - {self.ratingItemCode} - {self.ExhibitName}"
