from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from Messages.models import Message
from Users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = SerializerMethodField()

    class Meta:
        model = Message
        fields = ('text', 'sender', 'time')

    def get_sender(self, obj):
        return UserSerializer(obj.participant.user).data
