from django.urls import path
from .views import ScoreDetailView, ScoreView

urlpatterns = [
    path('scores/', ScoreView.as_view(), name='game-list'),
    path('scores/<int:score_id>/', ScoreDetailView.as_view(), name='game-detail'),
]