from django.urls import path, include

from ClassRoom import routing as classroom_routing
from Messages import routing as messages_routing

websocket_urlpatterns = [
    *classroom_routing.websocket_urlpatterns,
    *messages_routing.websocket_urlpatterns,
]
