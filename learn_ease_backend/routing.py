from ClassRoom import routing as classroom_routing
from Messages import routing as messages_routing
from Documents import routing as documents_routing
from Whiteboard import routing as whiteboard_routing
from Activities import routing as grades_routing
from VideoCall import routing as video_call_routing

websocket_urlpatterns = [
    *classroom_routing.websocket_urlpatterns,
    *messages_routing.websocket_urlpatterns,
    *documents_routing.websocket_urlpatterns,
    *whiteboard_routing.websocket_urlpatterns,
    *grades_routing.websocket_urlpatterns,
    *video_call_routing.websocket_urlpatterns,
]
