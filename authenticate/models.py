from django.db import models
from django.contrib.auth.models import User


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


# class Userprofile(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     user_roles = models.ManyToManyField('UserRole', related_name='users')


# class UserRole(models.Model):
#     ROLE_CHOICES = [
#         ('dm', 'District Manager'),
#         ('pm', 'Product Manager'),
#         ('sm', 'State Manager'),
#     ]

#     name = models.CharField(max_length=2, choices=ROLE_CHOICES, unique=True)
#     permissions = models.ManyToManyField('Permission', related_name='roles')

#     def __str__(self):
#         return dict(self.ROLE_CHOICES)[self.name]


# class Permission(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name
