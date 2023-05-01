from django.core.validators import MaxValueValidator
from django.db import models

class homepagemodel(models.Model):
    content = models.CharField(max_length=2000,blank=False)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)


class feedbackpagemodel(models.Model):
    Username = models.CharField(max_length=120,blank=True)
    Email = models.EmailField(max_length=120,blank=False)
    Feedback = models.TextField()
    created_at = models.DateField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)