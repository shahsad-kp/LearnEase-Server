from django.urls import path, include

from ClassRoom import routing as classroom_routing

websocket_urlpatterns = [
    *classroom_routing.websocket_urlpatterns
]
