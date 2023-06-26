from django.urls import path

from ClassRoom.consumer import ClassRoomConsumer

websocket_urlpatterns = [
    path('ws/classroom/<int:room_id>/', ClassRoomConsumer.as_asgi(), name='ClassRoom'),
]
