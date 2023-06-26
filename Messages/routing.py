from django.urls import path

from Messages.consumer import MessageConsumer

websocket_urlpatterns = [
    path('ws/messages/<int:room_id>/', MessageConsumer.as_asgi(), name='Messages'),
]
