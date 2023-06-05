from django.shortcuts import render, redirect
from .forms import RuleSetForm, RuleGroupForm, ActionFormSet
from .models import *

from django.forms import inlineformset_factory


def createRule(request):
    RuleGroupFormSet = inlineformset_factory(
        RuleSet, RuleGroup, form=RuleGroupForm, extra=1, can_delete=True)

    if request.method == 'POST':
        ruleset_form = RuleSetForm(request.POST, prefix='ruleset')
        rulegroup_formset = RuleGroupFormSet(request.POST, prefix='rulegroup')
        action_formset = ActionFormSet(request.POST, prefix='action')

        if (
            ruleset_form.is_valid() and
            rulegroup_formset.is_valid() and
            action_formset.is_valid()
        ):
            ruleset = ruleset_form.save()

            for form in rulegroup_formset:
                rulegroup = form.save(commit=False)
                rulegroup.ruleset = ruleset  # Assign the RuleSet instance
                rulegroup.save()
                form.save_m2m()

                for rule_form in form.nested:
                    rule = rule_form.save(commit=False)
                    rule.rulegroup = rulegroup  # Assign the RuleGroup instance
                    rule.save()

            for form in action_formset:
                action = form.save(commit=False)
                action.save()
                form.save_m2m()
                ruleset.actions.add(action)

            return redirect('viewRule', ruleset_id=ruleset.id)
    else:
        ruleset_form = RuleSetForm(prefix='ruleset')
        rulegroup_formset = RuleGroupFormSet(prefix='rulegroup')
        action_formset = ActionFormSet(prefix='action')

    return render(request, 'rulesmanager/createrule.html', {
        'ruleset_form': ruleset_form,
        'rulegroup_formset': rulegroup_formset,
        'action_formset': action_formset,
    })


def viewRule(request, ruleset_id):
    ruleset = RuleSet.objects.get(id=ruleset_id)
    return render(request, 'rulesmanager/viewrules.html', {'ruleset': ruleset})


def rulesmanager(request):
    options = ['createrule', 'viewrule']

    context = {'options': options, 'appLabel': 'rulesmanager'}
    return render(request, 'rulesmanager/home.html', context)
