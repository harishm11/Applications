from django.db import models
from systemtables.models import coverage
from ratemanager.models.ratingexhibits import RatingExhibits
from ratemanager.models.ratingvariables import RatingVariables


class RatebookTemplate(models.Model):
    RatebookID = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        default=None,
        editable=False
    )

    RatebookExhibit = models.ForeignKey(
        RatingExhibits,
        on_delete=models.CASCADE,
        verbose_name='Exhibits Belonging to this Ratebook'
    )
    ExhibitVariables = models.ManyToManyField(
        RatingVariables,
        verbose_name='Variables belonging to this Exhibit'
    )
    ExhibitCoverages = models.ManyToManyField(
        coverage.Coverage,
        verbose_name='Coverages belonging to this Exhibit'
    )
