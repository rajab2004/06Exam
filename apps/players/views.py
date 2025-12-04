from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpRequest
import json
from .models import Player
# Create your views here.

class PlayerView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            nickname = data.get('nickname')
            country = data.get('country')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        if not nickname or not country:
            return JsonResponse({"error": "Nickname and country are required"}, status=400)
        
        try:
            new_player = Player(
                nickname=nickname,
                country=country.capitalize()
            )
            new_player.save()
            return JsonResponse({
                "id": new_player.pk,
                "nickname": new_player.nickname,
                "country": new_player.country,
                "rating": 0,
                "created_at": new_player.created_at.isoformat()
                }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    def get(self, request):
    
        country = request.GET.get('country')
        min_rating = request.GET.get('min_rating')
        search = request.GET.get('search')

        players_list = Player.objects.all()

        if country:
            players_list = players_list.filter(country=country.capitalize())

        if min_rating:
            try:
                min_rating = int(min_rating)
                filtered_players = []
                for player in players_list:
                    if player.rating >= min_rating:
                        filtered_players.append(player)
                players_list = filtered_players
            except ValueError:
                return JsonResponse({"error": "minimal reyting son bulishi kerak"}, status=400)

        if search:
            filtered_players = []
            for player in players_list:
                if player.nickname == search:
                    filtered_players.append(player)
            players_list = filtered_players

        players_list = [player.to_dict() for player in players_list]
        return JsonResponse({
            "count": len(players_list),
            "results": players_list
            }, status=200)
    
class PlayerDetailView(View):
    
    def get(self, request: HttpRequest, player_id):
        try:
            player = get_object_or_404(Player, pk=player_id)
            return JsonResponse(player.to_dict(), status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)
    
    def put(self, request, player_id):
        try:
            data = json.loads(request.body) if request.body else {}
            player = get_object_or_404(Player, pk=player_id)
            
            player.nickname = data.get('nickname', player.nickname)
            player.country = data.get('country', player.country)
            
            player.save()
            return JsonResponse(player.to_dict(), status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)
        
    def delete(self, request, player_id):
        try:
            player = get_object_or_404(Player, pk=player_id)
            scores_count = player.scores.count()
            
            if scores_count > 0:
                return JsonResponse({'status': f'Cannot delete player with game history. Player has {scores_count} recorded games.'}, status=400)
            player.delete()
            return JsonResponse({'status': 'Deleted'}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404) 