from rest_framework.serializers import ModelSerializer

from Whiteboard.models import Whiteboard


class WhiteboardSerializer(ModelSerializer):
    class Meta:
        model = Whiteboard
        fields = ('id', 'room_id', 'data', 'created_at', 'updated_at')