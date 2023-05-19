# from django import forms
# from django.forms import formset_factory, BaseFormSet
# from .models import Rule, RuleGroup, Action, RuleSet


# class RuleForm(forms.ModelForm):
#     class Meta:
#         model = Rule
#         fields = ['field', 'operator', 'value']


# class RuleGroupForm(forms.ModelForm):
#     class Meta:
#         model = RuleGroup
#         fields = ['operator', 'rules']
#         widgets = {
#             'rules': forms.CheckboxSelectMultiple()
#         }


# class RuleSetForm(forms.ModelForm):
#     class Meta:
#         model = RuleSet
#         fields = ['name', 'description', 'level', 'operator', 'groups']
#         widgets = {
#             'groups': forms.CheckboxSelectMultiple()
#         }


# class ActionForm(forms.ModelForm):
#     class Meta:
#         model = Action
#         fields = ['type', 'record']


# class BaseRuleGroupFormSet(BaseFormSet):
#     def add_fields(self, form, index):
#         super().add_fields(form, index)
#         form.rules = RuleFormSet(
#             prefix=f'rule-group-{index}-rule',
#             data=self.data if self.is_bound else None,
#             files=self.files if self.is_bound else None
#         )


# class BaseRuleFormSet(BaseFormSet):
#     def add_fields(self, form, index):
#         super().add_fields(form, index)
#         form.field = forms.CharField()
#         form.operator = forms.CharField()
#         form.value = forms.CharField()


# RuleFormSet = formset_factory(RuleForm, extra=1, formset=BaseRuleFormSet)
# RuleGroupFormSet = formset_factory(
#     RuleGroupForm, extra=1, formset=BaseRuleGroupFormSet)
