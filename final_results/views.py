from django.shortcuts import render
from start_championship.models import Team

def final_results_view(request):
    teams = Team.objects.all()
    return render(request, 'final_results/final_results.html', {'teams': teams})
