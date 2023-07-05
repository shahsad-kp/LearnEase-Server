from django.db import models

from ClassRoom.models import ClassRoom, Participants


class Activity(models.Model):
    question = models.CharField(max_length=200)
    room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='activities')

    def __str__(self):
        return self.question


class Option(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.option} - {self.activity}"


class Response(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='responses')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='responses')
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE, related_name='responses')

    def __str__(self):
        return f"{self.option} - {self.participant}"
