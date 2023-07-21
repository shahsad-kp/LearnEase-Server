from channels.generic.websocket import AsyncJsonWebsocketConsumer


class VideoCallConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = None
        self.chat_room_group_name = None
        self.class_room_id = None
        self.user = None

    async def connect(self):
        await self.accept()
        if self.scope['user'].is_anonymous:
            await self.close(code=4001)
            return
        
        self.class_room_id = self.scope['url_route']['kwargs'].get('room_id')
        self.chat_room_group_name = f'videocall{self.class_room_id}'
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.chat_room_group_name,
            self.channel_name,
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_room_group_name,
            self.channel_name,
        )

    async def receive_json(self, content, **kwargs):
        match content['type']:
            case 'join':
                                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'join_student',
                        'from': self.user.id,
                    }
                )

            case 'offer':
                                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'offer',
                        'from': self.user.id,
                        'to': content['userId'],
                        'offer': content['offer'],
                    }
                )

            case 'answer':
                                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'answer',
                        'from': self.user.id,
                        'to': content['userId'],
                        'answer': content['answer'],
                    }
                )

            case 'ice-candidate':
                                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'ice_candidate',
                        'from': self.user.id,
                        'to': content['userId'],
                        'candidate': content['candidate'],
                    }
                )

            case _:
                pass

    async def join_student(self, event):
        if event['from'] == self.user.id: return
        await self.send_json(
            {
                'type': 'request-connection',
                'userId': event['from'],
            }
        )

    async def offer(self, event):
        if event['to'] != self.user.id:
            return
        await self.send_json(
            {
                'type': 'offer',
                'userId': event['from'],
                'offer': event['offer'],
            }
        )

    async def answer(self, event):
        if event['to'] != self.user.id:
            return
        await self.send_json(
            {
                'type': 'answer',
                'userId': event['from'],
                'answer': event['answer'],
            }
        )

    async def ice_candidate(self, event):
        if event['to'] != self.user.id:
            return
        await self.send_json(
            {
                'type': 'ice-candidate',
                'userId': event['from'],
                'candidate': event['candidate'],
            }
        )
