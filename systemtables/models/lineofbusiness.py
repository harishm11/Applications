from django.db import models


class LineOfBusiness(models.Model):
    LobName = models.CharField(
        max_length=255, null=True, blank=True, unique=True, verbose_name="LOB")

    def __str__(self):
        return self.LobName
