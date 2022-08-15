from django.core.validators import MaxValueValidator
from django.db import models

class policyModel(models.Model):
    quoteNumber = models.IntegerField(validators=[MaxValueValidator(999999999)], blank=False)
    policyNumber = models.IntegerField(validators=[MaxValueValidator(999999999)], blank=False)
    policyterm = models.IntegerField(validators=[MaxValueValidator(99)],blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class driverModel(models.Model):
    policyNumber=models.ForeignKey(policyModel,on_delete=models.CASCADE)
    driverFirstName = models.CharField(max_length=20,blank=False)
    driverLastName = models.CharField(max_length=20, blank=False)
    drivingExperience = models.IntegerField(validators=[MaxValueValidator(99)], blank=False)
    ageYears=models.IntegerField(validators=[MaxValueValidator(999)], blank=False)
    drivingCourse= models.BooleanField(default=False,blank=True)
    createdAt= models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

class vehicleModel(models.Model):
    policyNumber=models.ForeignKey(policyModel,on_delete=models.CASCADE)
    vehicleYear = models.IntegerField(validators=[MaxValueValidator(9999)], blank=False)
    vehicleMake = models.CharField(max_length=20,blank=False)
    vehicleMake = models.CharField(max_length=50,blank=False)
    annualMileage = models.CharField(max_length=5,blank=False)
    garagingZipCode = models.IntegerField(validators=[MaxValueValidator(99999)],blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class incidentModel(models.Model):
    policyNumber=models.ForeignKey(policyModel,on_delete=models.CASCADE)
    incidentDate = models.DateField(blank=False)
    incidentType = models.CharField(max_length=9, blank=False)
    involvedDriver = models.ForeignKey(driverModel,on_delete=models.CASCADE,related_name='involvedDriver')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)