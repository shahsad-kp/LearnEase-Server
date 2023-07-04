from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


@sync_to_async
def set_whiteboard_data(class_room_id, data):
    from Whiteboard.models import Whiteboard
    whiteboard, _ = Whiteboard.objects.update_or_create(
        room_id=class_room_id,
        defaults={
            'data': data
        }
    )
    whiteboard.data = data
    whiteboard.save()


class WhiteboardConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = None
        self.room_group_name = None
        self.user = None
        self.class_room_id = None

    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close(code=401)
            return

        self.class_room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'whiteboard{self.class_room_id}'
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        await self.close(code=404)

    async def receive_json(self, content, **kwargs):
        if content['type'] == 'new_data':
            await set_whiteboard_data(self.class_room_id, content['data'])
        elif content['type'] == 'clear_data':
            await set_whiteboard_data(self.class_room_id, None)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'clear_data',
                }
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                content
            )

    async def new_line(self, event):
        line = event['line']
        await self.send_json({
            'type': 'line',
            'line': line
        })

    async def clear_data(self, _):
        await self.send_json({
            'type': 'clear_data'
        })
