from django.urls import path
from .views import leaderboard, leaderboard_top, leaderboard_global

urlpatterns = [
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('leaderboard/top/', leaderboard_top, name='leaderboard-top'),
    path('leaderboard/global/', leaderboard_global, name='leaderboard-global'),

]