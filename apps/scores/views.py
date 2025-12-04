from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpRequest
import json
from .models import Scores

# Create your views here.
class ScoreView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            game_id = data.get('game')
            player_id = data.get('player')
            result = data.get('result')
            opponent_name = data.get('opponent_name', None)
            
            if not game_id or not player_id or result not in ['win', 'loss', 'draw']:
                return JsonResponse({"error": "game_id, player_id, result, are required"}, status=400)
            
            if result == 'win':
                points = 10
            elif result == 'draw':
                points = 5
            else:
                points = 0
            
            new_score = Scores(
                game_id=game_id,
                player_id=player_id,
                result=result,
                points=points,
                opponent_name=opponent_name
            )
            player = new_score.player
            if result == 'win':
                player.rating += 10
            elif result == 'draw':
                player.rating += 5
            player.save()
            new_score.save()
            return JsonResponse(new_score.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({"error": f"{str(e)}"}, status=400)
    
    def get(self, request):
        game_id = request.GET.get('game_id')
        player_id = request.GET.get('player_id')
        result = request.GET.get('result')
        
        scores_list = Scores.objects.all()
        if game_id:
            scores_list = scores_list.filter(game_id=game_id)
        if player_id:
            scores_list = scores_list.filter(player_id=player_id)
        if result:
            scores_list = scores_list.filter(result=result)
            
        scores_list = [score.to_dict() for score in scores_list]
        
        return JsonResponse({
            "count": len(scores_list),
            "results": scores_list
        }, status=200)
        
class ScoreDetailView(View):
    def get(self, request, score_id):
        try:
            score = get_object_or_404(Scores, pk=score_id)
            return JsonResponse(score.to_dict(), status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)
    
    def delete(self, request, score_id):
        try:
            score = get_object_or_404(Scores, pk=score_id)
            player = score.player
            result = score.result
            
            score.delete()
            
            if result == 'win':
                player.rating -= 10
            elif result == 'draw':
                player.rating -= 5
            player.save()
            
            return JsonResponse({"message": "Score deleted successfully"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=404)