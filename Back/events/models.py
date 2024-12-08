from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
