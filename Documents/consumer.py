from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DocumentConsumer(AsyncJsonWebsocketConsumer):
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
        self.room_group_name = f'document{self.class_room_id}'
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
        document = content['document']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'documents',
                'document': document,
            }
        )

    async def documents(self, event):
        document = event['document']
        await self.send_json({
            'document': document
        })
