from django.db import models


class State(models.Model):
    StateID = models.IntegerField()
    StateName = models.CharField(max_length=100)
    StateCode = models.CharField(max_length=2)
    ZipMin = models.CharField(max_length=5)
    ZipMax = models.CharField(max_length=5)
    EnableInd = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.StateCode}"