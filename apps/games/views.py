from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpRequest
import json
from .models import Game
from django.views import View
from django.core.exceptions import ValidationError

from datetime import datetime
# Create your views here.
class GameView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            title = data.get('title')
            location = data.get('location')
            start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
            description = data.get('description', None)
            
            if not title or not location:
                return JsonResponse({"error": "Title and location are required"}, status=400)
            
            new_game = Game(
                title=title,
                location=location,
                start_date=start_date,
                description=description
            )
            new_game.save()
            return JsonResponse(new_game.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({"error": f"{str(e)}"}, status=400)
    
    def get(self, request):
        games = Game.objects.all()
        games_list = [game.to_dict() for game in games]
        return JsonResponse({"games": games_list}, status=200)
    
class GameDetailView(View):
    
    def get(self, request, game_id):
        try:
            game = get_object_or_404(Game, pk=game_id)
            return JsonResponse(game.to_dict(), status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)
    
    def put(self, request, game_id):
        try:
            data = json.loads(request.body) if request.body else {}
            game = get_object_or_404(Game, pk=game_id)
            
            game.title = data.get('title', game.title)
            game.location = data.get('location', game.location)
            game.description = data.get('description', game.description)
        
            if 'start_date' in data:
                return JsonResponse({"error": "start datan ugartirib bulmaydi"}, status=400)
            
            game.save()
            return JsonResponse(game.to_dict(), status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)
        
    def delete(self, request, game_id):
        try:
            game = get_object_or_404(Game, pk=game_id)
            if game.game_scores.count() > 0:
                return JsonResponse({'status': 'Cannot delete game with existing scores. Tournament has active games.'}, status=400) 
            game.delete()
            return JsonResponse({'status': 'Deleted'}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)