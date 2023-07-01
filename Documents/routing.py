from django.urls import path

from Documents.consumer import DocumentConsumer

websocket_urlpatterns = [
    path('ws/documents/<int:room_id>/', DocumentConsumer.as_asgi()),
]
