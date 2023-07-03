from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from Whiteboard.models import Whiteboard


class GetWhiteBoardData(RetrieveAPIView):
    serializer_class = None
    permission_classes = [IsAuthenticated]
    lookup_field = 'room_id'
    lookup_url_kwarg = 'room_id'
    queryset = Whiteboard.objects.all()
