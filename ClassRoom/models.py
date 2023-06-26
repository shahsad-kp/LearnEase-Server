from django.db import models


class ClassRoom(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title + ' - ' + str(self.created_at)

    class Meta:
        ordering = ['-created_at']


class Topic(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.title + ' - ' + str(self.class_room)


class Participants(models.Model):
    room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE, related_name='participated_rooms')
    is_lecturer = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room.title + ' - ' + self.user.name + ' - ' + str(self.joined_at)

    class Meta:
        ordering = ['-joined_at']


class ParticipantRoomSettings(models.Model):
    participant = models.OneToOneField(Participants, on_delete=models.CASCADE, related_name='settings')
    audio_turned = models.BooleanField(default=False)
    video_turned = models.BooleanField(default=False)
    whiteboard_turned = models.BooleanField(default=False)
    audio_permission = models.BooleanField(default=True)
    video_permission = models.BooleanField(default=True)
    whiteboard_permission = models.BooleanField(default=True)

