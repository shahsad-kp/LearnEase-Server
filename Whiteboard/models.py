from django.db import models


class Whiteboard(models.Model):
    room_id = models.IntegerField()
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'whiteboards'
        ordering = ['-created_at']
