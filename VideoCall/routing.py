from django.urls import path

from .consumer import VideoCallConsumer

websocket_urlpatterns = [
    path('ws/video_call/<int:room_id>/', VideoCallConsumer.as_asgi()),
]
