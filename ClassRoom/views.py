from datetime import datetime, timedelta, date

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from ClassRoom.models import ClassRoom
from ClassRoom.serializers import ClassRoomSerializer, TopicSerializer


class CreateClassRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['lecturer'] = request.user.pk
        topics_data = data.pop('topics', [])

        serializer = ClassRoomSerializer(data=data)
        if serializer.is_valid():
            classroom = serializer.save(lecturer_id=request.user.pk)

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

        if not (classroom.lecturer == request.user or request.user in classroom.students.all()):
            return Response(status=HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(classroom)
        return Response(serializer.data)


class GetTopics(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopicSerializer

    def get(self, request, classroom_id):
        classroom = ClassRoom.objects.filter(id=classroom_id).first()
        if not classroom:
            return Response(status=HTTP_400_BAD_REQUEST)

        if not (classroom.lecturer == request.user or request.user in classroom.students.all()):
            return Response(status=HTTP_400_BAD_REQUEST)

        topics = classroom.topics.all()
        serializer = self.serializer_class(topics, many=True)
        return Response(serializer.data)


class GetHistory(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassRoomSerializer

    def get(self, request):
        last_week = datetime.today() - timedelta(days=7)
        classrooms = ClassRoom.objects.filter(
            Q(lecturer=request.user, created_at__gte=last_week) |
            Q(students=request.user, created_at__gte=last_week)
        ).filter(created_at__gte=last_week)
        serializer = self.serializer_class(classrooms, many=True)
        return Response(serializer.data)
