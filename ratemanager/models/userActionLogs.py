from django.db import models
from django.contrib.auth.models import User
from ratemanager.models.ratebookmetadata import RatebookMetadata

logID = models.AutoField(primary_key=True)
user = models.ForeignKey(User, on_delete=models.CASCADE)
ratebook = models.ForeignKey(RatebookMetadata, on_delete=models.CASCADE)
action = models.CharField()
createdAt = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.createdAt + self.user + self.action
