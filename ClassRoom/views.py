from datetime import datetime, timedelta, date

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from ClassRoom.models import ClassRoom, Participants
from ClassRoom.serializers import ClassRoomSerializer, TopicSerializer


class CreateClassRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['lecturer'] = request.user.pk
        topics_data = data.pop('topics', [])

        serializer = ClassRoomSerializer(data=data)
        if serializer.is_valid():
            classroom = serializer.save()
            Participants.objects.create(room=classroom, user=request.user, is_lecturer=True)
            for topic_data in topics_data:
                topic_data['class_room'] = classroom.id
                topic_serializer = TopicSerializer(data=topic_data)
                if topic_serializer.is_valid():
                    topic_serializer.save()

            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetClassRoom(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassRoomSerializer

    def get(self, request, classroom_id):
        classroom = ClassRoom.objects.filter(id=classroom_id).first()
        if not classroom:
            return Response(status=HTTP_400_BAD_REQUEST)

        # if not Participants.objects.filter(room=classroom, user=request.user).exists():
        #     return Response(status=HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(classroom)
        return Response(serializer.data)


class GetTopics(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopicSerializer

    def get(self, request, classroom_id):
        classroom = ClassRoom.objects.filter(id=classroom_id).first()
        if not classroom:
            return Response(status=HTTP_400_BAD_REQUEST)

        if not Participants.objects.filter(room=classroom, user=request.user).exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        topics = classroom.topics.all()
        serializer = self.serializer_class(topics, many=True)
        return Response(serializer.data)


class GetHistory(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassRoomSerializer

    def get(self, request):
        last_week = datetime.today() - timedelta(days=7)
        participates = request.user.participated_rooms.select_related('room').filter(room__created_at__gte=last_week)
        classrooms = [participate.room for participate in participates]
        serializer = self.serializer_class(classrooms, many=True)
        return Response(serializer.data)
