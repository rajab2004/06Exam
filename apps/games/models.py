from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=200 , null=False, blank=False, unique=True)
    location = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'game'
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'
        ordering = ['created_at']
        
    def to_dict(self):
        return {
            "id": self.pk,
            "title": self.title,
            "location": self.location,
            "start_date": self.start_date.isoformat(),
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }
        