from django.db import models


class Homepagemodel(models.Model):
    Content = models.CharField(max_length=2000, blank=False)
    CreateDate = models.DateField(auto_now_add=True, blank=True, null=True)
    UpdateDate = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.Content


class Feedbackmodel(models.Model):
    Username = models.CharField(max_length=120, blank=True)
    Email = models.EmailField(max_length=120, blank=False)
    Feedback = models.TextField()
    CreateDate = models.DateField(auto_now_add=True, blank=True, null=True)
    UpdateDate = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.Email, self.Feedback
