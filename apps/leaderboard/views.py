from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpRequest
from apps.scores.models import Scores
from apps.players.models import Player
from apps.games.models import Game

# Create your views here.



def leaderboard(request: HttpRequest):
    game_id = request.GET.get('game_id')
    if not game_id:
        return JsonResponse({"error": "game_id not faound"}, status=400)
    
    Scores_list = list(Scores.objects.filter(game_id=game_id))
    
    player_temp_data = {}
    
    for score in Scores_list:
        player =  score.player
        if player.id not in player_temp_data:
            player_temp_data[player.id] = {
                "rank": 0,
                "player": player.nickname,
                "player_id": player.id,
                "country": player.country,
                "rating": player.rating,
                "points": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "rating_change": '+0'
            }
        if player.id in player_temp_data:
            if score.result == 'win':
                player_temp_data[player.id]["points"] += score.points
                player_temp_data[player.id]["wins"] += 1
            elif score.result == 'draw':
                player_temp_data[player.id]["points"] += score.points
                player_temp_data[player.id]["draws"] += 1
            elif score.result == 'loss':
                player_temp_data[player.id]["losses"] += 1
    
    result = []
    for key, player_data in player_temp_data.items():
        player_data['rating_change'] = f"+{str(player_data['points'])}"
        result.append(player_data)
        
    result = sorted(result, key=lambda x: x['points'],  reverse=True)
    for index, player_data in enumerate(result):
        player_data['rank'] = index + 1

    return JsonResponse({"leaderboard": result}, status=200)
        

def leaderboard_top(request: HttpRequest):
    game_id = request.GET.get('game_id')
    limit = request.GET.get('limit', 10)
    if not game_id:
        return JsonResponse({"error": "game_id not faound"}, status=400)
    
    Scores_list = list(Scores.objects.filter(game_id=game_id))
    game = Game.objects.get(pk=game_id)
    player_temp_data = {}
    
    for score in Scores_list:
        player =  score.player
        if player.id not in player_temp_data:
            player_temp_data[player.id] = {
                "rank": 0,
                "player": player.nickname,
                "player_id": player.id,
                "country": player.country,
                "rating": player.rating,
                "points": 0,
            }
        if player.id in player_temp_data:
            if score.result == 'win':
                player_temp_data[player.id]["points"] += score.points
            elif score.result == 'draw':
                player_temp_data[player.id]["points"] += score.points
            else:
                pass
    
    result = []
    for key, player_data in player_temp_data.items():
        player_data['rating_change'] = f"+{str(player_data['points'])}"
        result.append(player_data)
        
    result = sorted(result, key=lambda x: x['points'],  reverse=True)
    for index, player_data in enumerate(result):
        player_data['rank'] = index + 1

    if limit:
        try:
            limit = int(limit)
            if limit > len(result):
                limit = len(result)
        except ValueError:
            return JsonResponse({"error": "limit son bulishi kerak"}, status=400)
        
    return JsonResponse({
        "game_id": game.pk,
        "game_title": game.title,
        "limit": limit,
        "total_players": len(result),
        "leaderboard": result[:limit]}, 
    status=200)
        
def leaderboard_global(request: HttpRequest):
    country = request.GET.get('country')
    limit = request.GET.get('limit', 100)
    
    try:
        limit = int(limit)
    except ValueError:
        return JsonResponse({"error": "limit son bulishi kerak"}, status=400)
    if country:
        players = Player.objects.filter(country=country.capitalize())
        total_country_scores = Player.objects.filter(country=country.capitalize()).count()
    else:
        players = Player.objects.all()
    
    player_temp_data = {}
    for player in players:
        player_scores = Scores.objects.filter(player_id=player.id).all()
        if player.id not in player_temp_data:
            player_temp_data[player.id] = {
                "rank": 0,
                "player": player.nickname,
                "rating": player.rating,
                "total_games": len(player_scores),
            }
    result = []
    for key, player_data in player_temp_data.items():
        result.append(player_data)
        
    result = sorted(result, key=lambda x: x['rating'],  reverse=True)
    for index, player_data in enumerate(result):
        player_data['rank'] = index + 1
        
    if country:
        result = result[:limit]
        return JsonResponse(
            {
                "total_players": total_country_scores,
                "country": country,
                "leaderboard": result
            },
            status=200
        )
    if not country:
        players = Player.objects.count()
        return JsonResponse({
            "total_players": players,
            "leaderboard": result[:limit]
        },
        status=200
    )