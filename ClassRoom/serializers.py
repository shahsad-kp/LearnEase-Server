from rest_framework.serializers import ModelSerializer

from ClassRoom.models import ClassRoom, Topic
from Users.serializers import UserSerializer


class ClassRoomSerializer(ModelSerializer):
    lecturer = UserSerializer(read_only=True)
    students = UserSerializer(read_only=True, many=True)

    class Meta:
        model = ClassRoom
        fields = ['id', 'title', 'lecturer', 'students', 'created_at']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'content', 'class_room']
