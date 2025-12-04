from django.db import models

# Create your models here.
class Player(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=50, blank=False, null=False)
    rating = models.IntegerField(default=0, )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def to_dict(self):
        scores = self.player_scores.all()
        if scores.exists():
            total_games = scores.count()
            wins = scores.filter(result='win').count()
            draws = scores.filter(result='draw').count()
            losses = scores.filter(result='loss').count()
        else:
            total_games = 0
            wins = 0
            draws = 0
            losses = 0
        return {
            "id": self.pk,
            "nickname": self.nickname,
            "country": self.country,
            "rating": self.rating,
            "total_games": total_games,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "created_at": self.created_at.isoformat()
        }