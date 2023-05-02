from django.db import models


class Statemodel(models.Model):
    StateID = models.AutoField(primary_key=True)
    StateName = models.CharField(max_length=100)
    StateCode = models.CharField(max_length=2)
    ZipMin = models.CharField(max_length=5)
    ZipMax = models.CharField(max_length=5)

    def __str__(self):
        return self.StateName, self.StateCode
