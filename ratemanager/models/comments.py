from django.db import models
from django.contrib.auth.models import User
from ratemanager.models.ratebookmetadata import RatebookMetadata


class Notes(models.Model):
    Ratebook = models.ForeignKey(RatebookMetadata, on_delete=models.CASCADE)
    Category = models.CharField(
        null=True, max_length=30, default=None,
        choices=(('Revision', 'Revision'),
                 ('Review', 'Review'))
        )
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Note = models.CharField(
        null=True,
        max_length=255,
        default=None,
        verbose_name='Note'
        )
    CreationDateTime = models.DateTimeField(
        null=False,
        default=None,
        verbose_name='Creation DateTime'
    )
