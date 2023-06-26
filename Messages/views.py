from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from ClassRoom.models import ClassRoom, Participants
from Messages.models import Message
from Messages.serializer import MessageSerializer


class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, classroom_id):
        classroom = ClassRoom.objects.filter(id=classroom_id).first()
        if not classroom:
            return Response(status=HTTP_400_BAD_REQUEST)

        if not Participants.objects.filter(room=classroom, user=request.user).exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        messages = Message.objects.filter(participant__room_id=classroom.id)
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)
