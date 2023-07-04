from django.db import models

from ClassRoom.models import ClassRoom, Participants


class Activity(models.Model):
    question = models.CharField(max_length=200)
    room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answer(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class Response(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer.answer
