from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from ClassRoom.models import ClassRoom, Topic, Participants


class ParticipantSettingsSerializer(ModelSerializer):
    audio = SerializerMethodField()
    video = SerializerMethodField()
    whiteboard = SerializerMethodField()

    class Meta:
        model = Participants
        fields = ['audio', 'video', 'whiteboard']

    def get_audio(self, obj):
        return {
            'permission': obj.audio_permission,
            'enabled': obj.audio_turned,
        }

    def get_video(self, obj):
        return {
            'permission': obj.video_permission,
            'enabled': obj.video_turned,
        }

    def get_whiteboard(self, obj):
        return {
            'permission': obj.whiteboard_permission,
            'enabled': obj.whiteboard_turned,
        }


class ParticipantSerializer(ModelSerializer):
    name = SerializerMethodField()
    profilePicture = SerializerMethodField()
    email = SerializerMethodField()
    settings = SerializerMethodField()
    id = SerializerMethodField()
    isActive = SerializerMethodField()

    class Meta:
        model = Participants
        fields = ['id', 'name', 'profilePicture', 'isActive', 'email', 'settings']

    def get_id(self, obj):
        return obj.user.id

    def get_name(self, obj):
        return obj.user.name

    def get_profilePicture(self, obj):
        return obj.user.profile_pic.url if obj.user.profile_pic else None

    def get_email(self, obj):
        return obj.user.email

    def get_settings(self, obj: Participants):
        settings = obj.settings
        return ParticipantSettingsSerializer(settings).data

    def get_isActive(self, obj):
        return obj.is_active


class ClassRoomSerializer(ModelSerializer):
    lecturer = SerializerMethodField()
    students = SerializerMethodField()

    class Meta:
        model = ClassRoom
        fields = ['id', 'title', 'lecturer', 'students', 'created_at']

    def get_lecturer(self, obj):
        lecturer = obj.participants.filter(is_lecturer=True).first()
        return ParticipantSerializer(lecturer).data

    def get_students(self, obj):
        students = []
        for student in obj.participants.filter(is_lecturer=False):
            students.append(ParticipantSerializer(student).data)
        return students


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'content', 'class_room']
