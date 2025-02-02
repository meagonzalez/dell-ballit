# Generated by Django 5.0.7 on 2024-08-03 22:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_team', '0001_initial'),
        ('start_championship', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='team_b',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_team_b', to='register_team.team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_matches', to='register_team.team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='team_a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_team_a', to='register_team.team'),
        ),
        migrations.AlterField(
            model_name='championship',
            name='teams',
            field=models.ManyToManyField(to='register_team.team'),
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
