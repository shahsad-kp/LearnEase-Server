from channels.generic.websocket import AsyncJsonWebsocketConsumer


class VideoCallConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = None
        self.chat_room_group_name = None
        self.class_room_id = None
        self.user_id = None

    async def connect(self):
        self.class_room_id = self.scope['url_route']['kwargs'].get('room_id')
        self.user_id = self.scope['url_route']['kwargs'].get('user_id')
        if not self.class_room_id:
            return await self.close(code=4004)
        self.chat_room_group_name = f'videocall{self.class_room_id}'

        await self.channel_layer.group_add(
            self.chat_room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_room_group_name,
            self.channel_name,
        )
        await self.close(code=404)

    async def receive_json(self, content, **kwargs):
        match content['type']:
            case 'join':
                print(f'user {self.user_id} join room {self.class_room_id}')
                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'join_student',
                        'from': self.user_id,
                    }
                )

            case 'offer':
                print(f'user {self.user_id} send offer to {content["userId"]}')
                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'offer',
                        'from': self.user_id,
                        'to': content['userId'],
                        'offer': content['offer'],
                    }
                )

            case 'answer':
                print(f'user {self.user_id} send answer to {content["userId"]}')
                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'answer',
                        'from': self.user_id,
                        'to': content['userId'],
                        'answer': content['answer'],
                    }
                )

            case 'ice-candidate':
                print(f'user {self.user_id} send ice candidate to {content["userId"]}')
                await self.channel_layer.group_send(
                    self.chat_room_group_name,
                    {
                        'type': 'ice_candidate',
                        'from': self.user_id,
                        'to': content['userId'],
                        'candidate': content['candidate'],
                    }
                )

            case _:
                pass

    async def join_student(self, event):
        if event['from'] == self.user_id: return
        await self.send_json(
            {
                'type': 'request-connection',
                'userId': event['from'],
            }
        )
        print(f'sended request to {event["from"]}')

    async def offer(self, event):
        if event['to'] != self.user_id:
            return
        await self.send_json(
            {
                'type': 'offer',
                'userId': event['from'],
                'offer': event['offer'],
            }
        )
        print(f'sended offer to {event["from"]}')

    async def answer(self, event):
        if event['to'] != self.user_id:
            return
        await self.send_json(
            {
                'type': 'answer',
                'userId': event['from'],
                'answer': event['answer'],
            }
        )
        print(f'sended answer to {event["from"]}')

    async def ice_candidate(self, event):
        if event['to'] != self.user_id:
            return
        await self.send_json(
            {
                'type': 'ice-candidate',
                'userId': event['from'],
                'candidate': event['candidate'],
            }
        )
        print(f'sended ice-candidate to {event["from"]}')
