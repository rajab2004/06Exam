from django.urls import path
from .views import GameView, GameDetailView

urlpatterns = [
    path('games/', GameView.as_view(), name='game-list'),
    path('games/<int:game_id>/', GameDetailView.as_view(), name='game-detail'),
]