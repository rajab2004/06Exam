from django.urls import path
from .views import PlayerView, PlayerDetailView

urlpatterns = [
    path('players/', PlayerView.as_view(), name='players'),
    path('players/<int:player_id>/', PlayerDetailView.as_view(), name='player-detail'),
]