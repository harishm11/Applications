from django.db import models
from systemtables.models import state, carrier, lineofbusiness, uwcompany


class RatebookGroups (models.Model):
    id = models.AutoField(
        primary_key=True,
        null=False,
        auto_created=True
        )
    Carrier = models.ForeignKey(
        carrier.Carrier,
        on_delete=models.CASCADE
        )
    State = models.ForeignKey(
        state.State,
        on_delete=models.CASCADE
        )
    LoBusiness = models.ForeignKey(
        lineofbusiness.LineOfBusiness,
        on_delete=models.CASCADE
        )
    UwCompany = models.ForeignKey(
        uwcompany.Uwcompany,
        on_delete=models.CASCADE
        )
    ProductGroup = models.CharField(max_length=50, null=True)
    ProductType = models.CharField(max_length=50, null=True)
    ProductName = models.CharField(max_length=50, null=True)
    ProjectID = models.CharField(max_length=50, null=True)
    RenewalEffDate = models.DateTimeField(null=False)
    RenewalExpDate = models.DateTimeField(null=False)
    ActivationDate = models.DateTimeField(null=False)
    ActivationTime = models.DateTimeField(null=False)

    def __str__(self):
        return str(self.id)


class RateBooks (models.Model):
    id = models.AutoField(primary_key=True,
                          null=False,
                          auto_created=True
                          )
    RatebookGroup = models.ForeignKey(
        RatebookGroups,
        on_delete=models.CASCADE
    )
    RatebookVersion = models.IntegerField(null=False)

    def __str__(self):
        return str(self.id)


class AllExhibits (models.Model):
    Ratebook = models.ForeignKey(
        RateBooks,
        on_delete=models.CASCADE
    )
    Coverage = models.CharField(max_length=100, null=True)
    Exhibit = models.CharField(max_length=100, null=True)
    Factor = models.CharField(max_length=100, null=True)
    RatingVarName1 = models.CharField(max_length=100, null=True)
    RatingVarName2 = models.CharField(max_length=100, null=True)
    RatingVarValue1 = models.CharField(max_length=100, null=True)
    RatingVarValue2 = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.Exhibit
