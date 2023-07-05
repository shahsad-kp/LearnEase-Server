from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


@sync_to_async
def create_activity(data, room_id):
    from Activities.models import Activity, Option
    from Activities.serializers import ActivitySerializer

    activity = Activity.objects.create(
        question=data['question'],
        room_id=room_id
    )
    for option in data['options']:
        Option.objects.create(
            activity=activity,
            option=option,
            correct=option == data['correctAnswer']
        )
    return ActivitySerializer(activity).data


@sync_to_async
def register_response(data, user_id, room_id):
    from Activities.models import Response
    from Activities.serializers import ResponseSerializer
    from ClassRoom.models import Participants

    participant = Participants.objects.filter(user_id=user_id, room_id=room_id).first()
    if not participant:
        return None

    response = Response.objects.create(
        activity_id=data['activityId'],
        option_id=data['optionId'],
        participant=participant
    )
    return ResponseSerializer(response).data


class ActivityConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = None
        self.chat_room_group_name = None
        self.user = None
        self.class_room_id = None

    async def connect(self):
        if self.scope['user'].is_anonymous:
            return await self.close(code=4004)

        self.class_room_id = self.scope['url_route']['kwargs']['room_id']
        self.chat_room_group_name = f'activities_{self.class_room_id}'
        self.user = self.scope['user']

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
        if content['type'] == 'new_activity':
            activity = await create_activity(content['activity'], self.class_room_id)
            await self.channel_layer.group_send(
                self.chat_room_group_name,
                {
                    'type': 'new_activity',
                    'activity': activity
                }
            )
        elif content['type'] == 'new_response':
            response = await register_response(content['data'], self.user.id, self.class_room_id)
            if not response:
                return await self.close(code=4004)
            await self.channel_layer.group_send(
                self.chat_room_group_name,
                {
                    'type': 'new_response',
                    'response': response
                }
            )
        pass

    async def new_activity(self, event):
        await self.send_json(event)

    async def new_response(self, event):
        await self.send_json(event)
