from django.urls import path

from Activities.consumer import ActivityConsumer

websocket_urlpatterns = [
    path('ws/activities/<int:room_id>/', ActivityConsumer.as_asgi(), name='Activities'),
]
