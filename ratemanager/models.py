from django.db import models


class RatebookGroups (models.Model):
    id = models.IntegerField(primary_key=True, null=False,
                             auto_created=True, default=0)
    state = models.CharField(max_length=50, null=True)
    business = models.CharField(max_length=50, null=True)
    company = models.CharField(max_length=50, null=True)
    product_group = models.CharField(max_length=50, null=True)
    product_type = models.CharField(max_length=50, null=True)
    product_name = models.CharField(max_length=50, null=True)
    projectid = models.CharField(max_length=50, null=True)
    ratebookgroupid = models.CharField(max_length=50, null=True)


class RateBooks (models.Model):
    id = models.IntegerField(primary_key=True, null=False,
                             auto_created=True, default=0)
    ratebookgroupid = models.CharField(max_length=50, null=True)
    ratebookid = models.CharField(max_length=50, null=True)
    ratebookversion = models.CharField(max_length=50, null=True)


class AllExhibits (models.Model):
    id = models.IntegerField(primary_key=True, null=False,
                             auto_created=True, default=0)
    ratebookid = models.CharField(max_length=100)
    Coverage = models.CharField(max_length=100, null=True)
    Exhibit = models.CharField(max_length=100, null=True)
    Factor = models.CharField(max_length=100, null=True)
    RatingVarName1 = models.CharField(max_length=100, null=True)
    RatingVarName2 = models.CharField(max_length=100, null=True)
    RatingVarValue1 = models.CharField(max_length=100, null=True)
    RatingVarValue2 = models.CharField(max_length=100, null=True)
