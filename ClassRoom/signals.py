from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ClassRoom.models import Participants, ParticipantRoomSettings


@receiver(post_save, sender=Participants)
def create_participant_room_settings(sender, instance, created, **kwargs):
    if created:
        print('ParticipantRoomSettings created')
        ParticipantRoomSettings.objects.create(participant=instance)
