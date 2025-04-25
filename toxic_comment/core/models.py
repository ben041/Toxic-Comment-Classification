from django.db import models
from django.contrib.auth.models import User

class AnalysisHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    toxicity_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_toxic = models.BooleanField()

    class Meta:
        ordering = ['-created_at']
