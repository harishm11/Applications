from django import forms
from django.forms import formset_factory, BaseFormSet
from .models import Rule, RuleGroup, Action, RuleSet
from django import forms
from .models import RuleSet, RuleGroup, Rule, Action

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['Rulefield', 'Ruleoperator', 'Rulevalue']

class RuleGroupForm(forms.ModelForm):
    class Meta:
        model = RuleGroup
        fields = ['RuleGroupOperator']

RuleGroupFormSet = forms.inlineformset_factory(
    RuleGroup,
    Rule,
    form=RuleForm,
    fields=['Rulefield', 'Ruleoperator', 'Rulevalue'],
    extra=1,
    can_delete=True,
)

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['ActionType', 'ActionMessage']

ActionFormSet = forms.inlineformset_factory(
    RuleSet,
    Action,
    form=ActionForm,
    fields=['ActionType', 'ActionMessage'],
    extra=1,
    can_delete=True,
)

class RuleSetForm(forms.ModelForm):
    class Meta:
        model = RuleSet
        fields = ['RulesetName', 'RulesetDescription', 'RulesetLevel', 'RulesetOperator']
