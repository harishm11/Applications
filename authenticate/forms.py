from django.contrib.auth.models import Group
from .models import *
from django import forms


class feedbackpageform(forms.ModelForm):
    class Meta:
        model = Feedbackmodel
        exclude = []
        widgets = {
            'Username': forms.TextInput(attrs={'type': 'hidden'})
        }


class SwitchGroupForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=Group.objects.none(),  # Initialize as an empty queryset
        empty_label=None  # Remove the empty label
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the queryset to include only groups the user is a member of
        self.fields['group'].queryset = user.groups.order_by('name')
