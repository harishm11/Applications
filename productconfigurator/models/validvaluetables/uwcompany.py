from django.db import models
class Uwcompany(models.Model):
    CompanyName = models.CharField(max_length=255,null=True,blank=True)
