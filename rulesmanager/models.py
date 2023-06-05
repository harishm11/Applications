# models.py
from django.db import models


class Rule(models.Model):
    Rulefield = models.CharField(max_length=255)
    Ruleoperator = models.CharField(max_length=255)
    Rulevalue = models.CharField(max_length=255)
    RuleGroup = models.ForeignKey('RuleGroup', on_delete=models.CASCADE)


class RuleGroup(models.Model):
    RuleGroupOperator = models.CharField(max_length=255, blank=True)
    Rules = models.ManyToManyField(Rule)
    Ruleset = models.ForeignKey('RuleSet', on_delete=models.CASCADE)


class Action(models.Model):
    ActionType = models.CharField(max_length=255)
    ActionMessage = models.CharField(max_length=255, blank=True)
    Ruleset = models.ForeignKey('RuleSet', on_delete=models.CASCADE)


class RuleSet(models.Model):
    RulesetName = models.CharField(max_length=255)
    RulesetDescription = models.TextField()
    RulesetLevel = models.CharField(max_length=255)
    RulesetOperator = models.CharField(max_length=255, blank=True)
    Groups = models.ManyToManyField(RuleGroup)
    Actions = models.ManyToManyField(Action)
