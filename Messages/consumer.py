from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


@sync_to_async
def add_message_to_db(message, user_id, room_id):
    from .models import Message
    from ClassRoom.models import Participants
    from .serializer import MessageSerializer
    try:
        participant = Participants.objects.filter(user_id=user_id, room_id=room_id).first()
    except Participants.DoesNotExist:
        raise KeyError('Participant does not exist')
    message = Message.objects.create(text=message, participant=participant)
    message.save()
    return MessageSerializer(message).data


class MessageConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = None
        self.room_group_name = None
        self.user = None
        self.class_room_id = None

    async def connect(self):
        await self.accept()
        if self.scope['user'].is_anonymous:
            await self.close(code=4001)
            return

        self.class_room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'message{self.class_room_id}'
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive_json(self, content, **kwargs):
        message = content['message']
        message_data = await add_message_to_db(message, self.user.id, self.class_room_id)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_data,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send_json({
            'message': message
        })
