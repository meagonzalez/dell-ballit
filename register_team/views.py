from django.shortcuts import render, redirect
from .forms import TeamForm

def register_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_team_success')
    else:
        form = TeamForm()
    return render(request, 'register_team/register_team.html', {'form': form})

def register_team_success(request):
    return render(request, 'register_team/success.html')


# Optionally: add logic to start a championship if relevant
def start_championship(request):
    return redirect('start_championship')  # Redirect to the start_championship view if this is the intention
""""
def start_championship(request):
    # Logic to get matches
    matches = ...  # Retrieve the matches
    return render(request, 'register_team/start_championship.html', {'matches': matches})

def view_scores(request):
    # Logic to get scores
    teams = ...  # Retrieve the team scores
    return render(request, 'register_team/view_scores.html', {'teams': teams})

def final_results(request):
    # Logic to get final results
    final_results = ...  # Retrieve the final results
    winning_team = ...  # Retrieve the winning team
    return render(request, 'register_team/final_results.html', {
        'final_results': final_results,
        'winning_team': winning_team
    })

"""