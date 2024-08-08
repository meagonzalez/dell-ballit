
from django.contrib import admin
from django.urls import path
from register_team import views as register_team_views
from start_championship import views as start_championship_views
from final_results import views as final_results_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface URL
    
    # Team Registration URLs
    path('', register_team_views.register_team, name='register_team'),  # Home page / team registration form
    path('register/success/', register_team_views.register_team_success, name='register_team_success'),  # Registration success page
    
    path('create/', start_championship_views.start_championship, name='start_championship'),
    path('choose/<int:championship_id>/', start_championship_views.choose_match, name='choose_match'),
    path('match/<int:match_id>/', start_championship_views.match_panel, name='match_panel'),
    
    path('final_results/', final_results_views.final_results_view, name='final_results'),

    # Additional URLs can be added here as needed
]