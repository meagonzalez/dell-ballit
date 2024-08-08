from django import forms
from .models import Championship, Match
from register_team.models import Team

class ChampionshipForm(forms.ModelForm):
    class Meta:
        model = Championship
        fields = []

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team_a', 'team_b']
