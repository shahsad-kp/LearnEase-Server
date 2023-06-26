from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


@sync_to_async
def add_participant(class_room_id: int, user_id: int):
    from ClassRoom.models import ClassRoom
    try:
        class_room = ClassRoom.objects.get(id=class_room_id)
    except ClassRoom.DoesNotExist:
        raise KeyError('ClassRoom does not exist')
    if (class_room.lecturer_id == user_id) or (user_id in class_room.students.all()):
        return
    print(user_id)
    class_room.students.add(user_id)
    class_room.save()


@sync_to_async
def remove_participant(class_room_id: int, user_id: int):
    from ClassRoom.models import ClassRoom
    from ClassRoom.serializers import ClassRoomSerializer
    try:
        class_room = ClassRoom.objects.get(id=class_room_id)
    except ClassRoom.DoesNotExist:
        raise KeyError('ClassRoom does not exist')
    if (class_room.lecturer_id != user_id) and (user_id not in class_room.students.all()):
        return ClassRoomSerializer(class_room).data
    class_room.students.remove(user_id)
    class_room.save()


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
            await add_participant(self.class_room_id, self.user.id)
        except KeyError:
            await self.close(code=404)
            return

        await self.channel_layer.group_send(
            self.chat_room_group_name,
            {
                'type': 'join_student',
                'user': {
                    'id': self.user.id,
                    'name': self.user.name,
                    'email': self.user.email,
                    'profile_pic': self.user.profile_pic.url if self.user.profile_pic else None,
                }
            }
        )
        await self.channel_layer.group_add(
            self.chat_room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room_group_name,
            self.channel_name
        )
        self.channel_layer.group_send(
            self.chat_room_group_name,
            {
                'type': 'leave_student',
                'user_id': self.user.id,
            }
        )

    async def receive_json(self, content, **kwargs):
        message = content.get('message')
        if message:
            await self.channel_layer.group_send(
                self.chat_room_group_name,
                {
                    'type': '',
                    'message': message,
                    'user': self.user.email
                }
            )

    async def join_student(self, event):
        await self.send_json(
            {
                'type': 'join_student',
                'user': event['user']
            }
        )

    async def leave_student(self, event):
        await self.send_json(
            {
                'type': 'leave_student',
                'user_id': event['user_id']
            }
        )
