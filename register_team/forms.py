# register_team/forms.py
from django import forms
from .models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'war_cry', 'foundation_year']
        widgets = {
            'foundation_year': forms.NumberInput(attrs={'placeholder': 'YYYY'}),
        }