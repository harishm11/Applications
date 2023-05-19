from django.forms import formset_factory
from .forms import *
from django.shortcuts import render, redirect
import json
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
from django.db import connection
import pandas as pd
from myproj.settings import BASE_DIR
from django.apps import apps


def rulesmanager(request):
    options = ['createrule', 'viewrule']

    context = {'options': options, 'appLabel': 'rulesmanager'}
    return render(request, 'rulesmanager/home.html', context)


# def createRule(request):
#     RuleGroupFormSet = formset_factory(
#         RuleGroupForm, extra=1, formset=BaseRuleGroupFormSet)
#     RuleFormSet = formset_factory(RuleForm, extra=1, formset=BaseRuleFormSet)

#     if request.method == 'POST':
#         rule_set_form = RuleSetForm(request.POST, prefix='rule-set')
#         action_form = ActionForm(request.POST, prefix='action')
#         rule_group_forms = RuleGroupFormSet(request.POST, prefix='rule-group')
#         rule_forms = RuleFormSet(request.POST, prefix='rule')

#         if (
#             rule_set_form.is_valid() and
#             action_form.is_valid() and
#             rule_group_forms.is_valid() and
#             rule_forms.is_valid()
#         ):
#             rule_set = rule_set_form.save()

#             for form in rule_group_forms:
#                 rule_group = form.save(commit=False)
#                 rule_group.rule_set = rule_set
#                 rule_group.save()

#                 for rule_form in form.rules:
#                     rule = rule_form.save()
#                     rule_group.rules.add(rule)

#             action = action_form.save(commit=False)
#             action.rule_set = rule_set
#             action.save()

#             return redirect('rule_created')

#     else:
#         rule_set_form = RuleSetForm(prefix='rule-set')
#         action_form = ActionForm(prefix='action')
#         rule_group_forms = RuleGroupFormSet(prefix='rule-group')
#         rule_forms = RuleFormSet(prefix='rule')

#     context = {
#         'rule_set_form': rule_set_form,
#         'action_form': action_form,
#         'rule_group_forms': rule_group_forms,
#         'rule_forms': rule_forms,
#     }

#     return render(request, 'rulesmanager/createrule.html', context)
