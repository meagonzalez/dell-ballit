# register_team/models.py
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    war_cry = models.CharField(max_length=255)
    foundation_year = models.PositiveIntegerField()

    # Optional fields for tracking team statistics
    blots = models.PositiveIntegerField(default=0)
    plifs = models.PositiveIntegerField(default=0)
    advrunghs = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=50)  # Default starting points

    def __str__(self):
        return self.name

    def update_points(self):
        # Update total points based on blots, plifs, and advrunghs
        self.total_points = 50 + (self.blots * 5) - (self.plifs * 1) - (self.advrunghs * 10)
        self.save()

    class Meta:
        ordering = ['-total_points']  # Order by total_points in descending order