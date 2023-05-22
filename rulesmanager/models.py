# # models.py
# from django.db import models


# class Rule(models.Model):
#     field = models.CharField(max_length=255)
#     operator = models.CharField(max_length=255)
#     value = models.CharField(max_length=255)


# class RuleGroup(models.Model):
#     operator = models.CharField(max_length=255, blank=True)
#     rules = models.ManyToManyField(Rule)


# class RuleSet(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     level = models.CharField(max_length=255)
#     operator = models.CharField(max_length=255, blank=True)
#     groups = models.ManyToManyField(RuleGroup)


# class Action(models.Model):
#     rule_set = models.ForeignKey(
#         RuleSet, on_delete=models.CASCADE, related_name='actions')
#     type = models.CharField(max_length=255)
#     record = models.CharField(max_length=255, blank=True)
