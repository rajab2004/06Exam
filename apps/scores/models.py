from django.db import models

# Create your models here.
class Scores(models.Model):
    choice = [
        ('win', 'Win'),
        ('loss', 'Loss'),
        ('draw', 'Draw'),
    ]
    game = models.ForeignKey('games.Game', on_delete=models.PROTECT, related_name='game_scores')
    player = models.ForeignKey('players.Player', on_delete=models.PROTECT, related_name='player_scores')
    result = models.CharField(max_length=10, choices=choice)
    points = models.IntegerField()
    opponent_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def to_dict(self):
        return {
            "id": self.pk,
            "game": {
                "id": self.game.id,
                "title": self.game.title
            },
            "player": {
                "id": self.player.id,
                "nickname": self.player.nickname
            },
            "result": self.result,
            "points": f"+{self.points}",
            "opponent_name": self.opponent_name,
            "created_at": self.created_at.isoformat()
        }