from django.urls import path

from Whiteboard.consumer import WhiteboardConsumer

websocket_urlpatterns = [
    path('ws/whiteboard/<int:room_id>/', WhiteboardConsumer.as_asgi()),
]
