from django.db import models


class RatingVariable(models.Model):
    RATING_VAR_TYPE_CHOICES = [
        ('Int', 'Integer'),
        ('Boolean', 'Boolean'),
        ('Varchar', 'String'),
    ]

    RatingVarName = models.CharField(max_length=100)
    Displayname = models.CharField(max_length=100, null=True, blank=True)
    RatingVarType = models.CharField(
        max_length=10, choices=RATING_VAR_TYPE_CHOICES, null=True, blank=True)
    RatingVarlength = models.IntegerField(null=True, blank=True, default=10)
    RatingVarFormat = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.RatingVarName
