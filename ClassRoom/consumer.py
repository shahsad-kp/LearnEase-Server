from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


@sync_to_async
def add_participant(class_room_id: int, user_id: int):
    from ClassRoom.models import ClassRoom, Participants
    from ClassRoom.serializers import ParticipantSerializer
    try:
        class_room = ClassRoom.objects.get(id=class_room_id)
    except ClassRoom.DoesNotExist:
        raise KeyError('ClassRoom does not exist')
    participant = class_room.participants.filter(user_id=user_id).first()
    if participant:
        return ParticipantSerializer(participant).data
    participant = Participants.objects.create(user_id=user_id, room_id=class_room_id)
    participant.save()
    return ParticipantSerializer(participant).data


@sync_to_async
def remove_participant(class_room_id: int, user_id: int):
    from ClassRoom.models import ClassRoom
    try:
        class_room = ClassRoom.objects.get(id=class_room_id)
    except ClassRoom.DoesNotExist:
        raise KeyError('ClassRoom does not exist')
    participant = class_room.participants.filter(user_id=user_id).first()
    if not participant:
        return
    if participant.is_lecturer:
        return
    participant.delete()


@sync_to_async
def change_settings(user_id: int, class_room_id: int, audio: bool, video: bool):
    from ClassRoom.models import Participants
    try:
        participant = Participants.objects.get(user_id=user_id, room_id=class_room_id)
    except Participants.DoesNotExist:
        raise KeyError('Participant does not exist')
    participant.settings.audio_turned = audio
    participant.settings.video_turned = video
    participant.settings.save()
    from ClassRoom.serializers import ParticipantSettingsSerializer
    return ParticipantSettingsSerializer(participant.settings).data


@sync_to_async
def change_permissions(user_id: int, target_user_id, class_room_id: int, audio: bool, video: bool):
    from ClassRoom.models import Participants
    try:
        Participants.objects.get(user_id=user_id, room_id=class_room_id, is_lecturer=True)
    except Participants.DoesNotExist:
        raise PermissionError('You are not a lecturer')
    try:
        participant = Participants.objects.get(user_id=target_user_id, room_id=class_room_id)
    except Participants.DoesNotExist:
        raise KeyError('Participant does not exist')

    if audio is not None:
        participant.settings.audio_permission = audio
    if video is not None:
        participant.settings.video_permission = video
    participant.settings.save()
    from ClassRoom.serializers import ParticipantSettingsSerializer
    return ParticipantSettingsSerializer(participant.settings).data


class ClassRoomConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = None
        self.chat_room_group_name = None
        self.user = None
        self.class_room_id = None

    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close(code=401)
            return
        self.class_room_id = self.scope['url_route']['kwargs']['room_id']
        self.chat_room_group_name = f'classroom_{self.class_room_id}'
        self.user = self.scope['user']

        try:
            participant = await add_participant(self.class_room_id, self.user.id)
        except KeyError:
            await self.close(code=404)
            return
        await self.channel_layer.group_send(
            self.chat_room_group_name,
            {
                'type': 'join_student',
                'student': participant,
            }
        )
        await self.channel_layer.group_add(
            self.chat_room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, event):
        if not self.user:
            return

        await self.channel_layer.group_send(
            self.chat_room_group_name,
            {
                'type': 'leave_student',
                'student_id': self.user.id,
            }
        )
        await self.channel_layer.group_discard(
            self.chat_room_group_name,
            self.channel_name,
        )
        try:
            await remove_participant(self.class_room_id, self.user.id)
        except KeyError:
            pass
        await self.close(code=404)

    async def receive_json(self, content, **kwargs):
        match content['type']:
            case 'change_settings':
                audio = content['audio']
                video = content['video']
                new_settings = await change_settings(self.user.id, self.class_room_id, audio, video)
                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'change_settings',
                        'user_id': self.user.id,
                        'settings': new_settings,
                    }
                )
            case 'change_permission':
                target_user_id = content['user_id']
                permissions = content['permission']
                audio = permissions.get('audio')
                video = permissions.get('video')
                try:
                    new_settings = await change_permissions(
                        self.user.id,
                        target_user_id,
                        self.class_room_id,
                        audio,
                        video
                    )
                except [KeyError, PermissionError]:
                    return
                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'change_settings',
                        'user_id': target_user_id,
                        'settings': new_settings,
                    }
                )

            case _:
                print('unknown message type', content['type'])

    async def join_student(self, event):
        await self.send_json(
            {
                'type': 'join_student',
                'student': event['student']
            }
        )

    async def leave_student(self, event):
        await self.send_json(
            {
                'type': 'leave_student',
                'student_id': event['student_id']
            }
        )

    async def change_settings(self, event):
        await self.send_json(
            {
                'type': 'change_settings',
                'user_id': event['user_id'],
                'settings': event['settings'],
            }
        )
