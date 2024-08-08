from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Championship, Match
from register_team.models import Team
import random

def start_championship(request):
    teams = list(Team.objects.all())
    
    if len(teams) < 8:
        messages.error(request, 'Not enough teams to start the championship.')
        return redirect('register_team')  # Redirect to the team registration view

    # Shuffle teams and create matches
    random.shuffle(teams)
    while len(teams) % 2 != 0:
        teams.pop()  # Ensure even number of teams

    # Create championship
    championship = Championship.objects.create()
    championship.teams.set(Team.objects.all())
    championship.save()

    phase = 1
    matches = []
    while len(teams) > 1:
        team_a = teams.pop()
        team_b = teams.pop()
        match = Match.objects.create(team_a=team_a, team_b=team_b, championship=championship, phase=phase)
        matches.append(match)
    
    context = {
        'matches': matches,
        'championship': championship
    }
    return render(request, 'start_championship/start_championship.html', context)

def choose_match(request, championship_id):
    championship = Championship.objects.get(id=championship_id)
    matches = Match.objects.filter(championship=championship, winner__isnull=True)
    
    if request.method == 'POST':
        match_id = request.POST.get('match_id')
        match = Match.objects.get(id=match_id)
        return redirect('match_panel', match_id=match.id)
    
    context = {
        'matches': matches,
        'championship': championship
    }
    return render(request, 'start_championship/choose_match.html', context)

def match_panel(request, match_id):
    match = Match.objects.get(id=match_id)
    
    # Ensure teams start with 50 points if not already set
    if match.team_a.total_points is None:
        match.team_a.total_points = 50
    if match.team_b.total_points is None:
        match.team_b.total_points = 50

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_score':
            team_a_score = int(request.POST.get('team_a_score'))
            team_b_score = int(request.POST.get('team_b_score'))
            
            match.team_a.total_points = team_a_score
            match.team_b.total_points = team_b_score
            
            if team_a_score > team_b_score:
                match.winner = match.team_a
            elif team_b_score > team_a_score:
                match.winner = match.team_b
            else:
                # Handle tie-breaking logic here
                team_a_war_cry_volume = int(request.POST.get('team_a_war_cry_volume'))
                team_b_war_cry_volume = int(request.POST.get('team_b_war_cry_volume'))
                
                if team_a_war_cry_volume > team_b_war_cry_volume:
                    match.team_a.total_points += 3
                    match.winner = match.team_a
                elif team_b_war_cry_volume > team_a_war_cry_volume:
                    match.team_b.total_points += 3
                    match.winner = match.team_b
                else:
                    # Handle further tie-breaking logic if there's enough time to develop
                    pass
            
            match.is_active = False
            match.team_a.save()
            match.team_b.save()
            match.save()
            progress_tournament(match)
        
        elif action == 'blot_a':
            match.team_a.blots += 1
            match.team_a.total_points += 5
        elif action == 'blot_b':
            match.team_b.blots += 1
            match.team_b.total_points += 5
        elif action == 'plif_a':
            match.team_a.plifs += 1
            match.team_a.total_points += 1
        elif action == 'plif_b':
            match.team_b.plifs += 1
            match.team_b.total_points += 1
        elif action == 'end_match':
            match.is_active = False
        
        match.team_a.save()
        match.team_b.save()
        match.save()
        return redirect('match_panel', match_id=match.id)

    context = {
        'match': match,
        'team_a': match.team_a,
        'team_b': match.team_b,
        'score_a': match.team_a.total_points,
        'score_b': match.team_b.total_points,
    }
    return render(request, 'start_championship/match_panel.html', context)

def progress_tournament(completed_match):
    if completed_match.is_active == False and completed_match.winner:
        # Find the next match for the winner
        next_match = Match.objects.filter(is_active=True, team_a__isnull=True).first()
        if next_match:
            next_match.team_a = completed_match.winner
            next_match.save()
        else:
            # Check if there's an active match with only one team
            waiting_match = Match.objects.filter(is_active=True, team_b__isnull=True).first()
            if waiting_match:
                waiting_match.team_b = completed_match.winner
                waiting_match.save()
            else:
                # Create a new match if no existing match is found
                Match.objects.create(team_a=completed_match.winner)
        
        # Check if there are no more matches left
        remaining_matches = Match.objects.filter(is_active=True)
        if not remaining_matches.exists():
            # Declare the final winner
            final_winner = completed_match.winner
            # Handle final winner logic here (e.g., update championship status)
            championship = completed_match.championship
            championship.winner = final_winner
            championship.save()