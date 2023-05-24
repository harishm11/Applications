from django.db import models


class RatebookGroups (models.Model):
    id = models.IntegerField(primary_key=True, null=False,
                             auto_created=True, default=0)
    State = models.CharField(max_length=50, null=True)
    LoBusiness = models.CharField(max_length=50, null=True)
    Company = models.CharField(max_length=50, null=True)
    ProductGroup = models.CharField(max_length=50, null=True)
    ProductType = models.CharField(max_length=50, null=True)
    ProductName = models.CharField(max_length=50, null=True)
    ProjectID = models.CharField(max_length=50, null=True)
    RatebookGroupID = models.CharField(max_length=50, null=True)


class RateBooks (models.Model):
    id = models.IntegerField(primary_key=True, null=False,
                             auto_created=True, default=0)
    RatebookGroupID = models.CharField(max_length=50, null=True)
    RatebookID = models.CharField(max_length=50, null=True)
    RatebookVersion = models.CharField(max_length=50, null=True)


class AllExhibits (models.Model):
    id = models.IntegerField(primary_key=True, null=False,
                             auto_created=True, default=0)
    RatebookID = models.CharField(max_length=100)
    Coverage = models.CharField(max_length=100, null=True)
    Exhibit = models.CharField(max_length=100, null=True)
    Factor = models.CharField(max_length=100, null=True)
    RatingVarName1 = models.CharField(max_length=100, null=True)
    RatingVarName2 = models.CharField(max_length=100, null=True)
    RatingVarValue1 = models.CharField(max_length=100, null=True)
    RatingVarValue2 = models.CharField(max_length=100, null=True)
