from django.db import models


class DynamicModel(models.Model):
    model_name = models.CharField(max_length=50)
    field_name = models.CharField(max_length=50)
    field_type = models.CharField(max_length=50)
