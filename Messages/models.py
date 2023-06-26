from django.db import models


class Message(models.Model):
    text = models.TextField()
    participant = models.ForeignKey('ClassRoom.Participants', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text} - {self.participant.user.name}'
