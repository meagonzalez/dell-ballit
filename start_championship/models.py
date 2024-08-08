from django.db import models
from register_team.models import Team

class Championship(models.Model):
    teams = models.ManyToManyField(Team)
    started = models.BooleanField(default=False, blank=True)
    
    def __str__(self):
        return f"Championship {self.id}"
        
class Match(models.Model):
    team_a = models.ForeignKey(Team, related_name='team_a', on_delete=models.CASCADE)
    team_b = models.ForeignKey(Team, related_name='team_b', on_delete=models.CASCADE)
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    phase = models.IntegerField()
    winner = models.ForeignKey(Team, related_name='match_wins', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.team_a} vs {self.team_b} - Phase {self.phase}"
