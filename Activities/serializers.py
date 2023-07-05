from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from Activities.models import Activity, Option
from Activities.models import Response


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'option')


class ResponseSerializer(serializers.ModelSerializer):
    activityId = serializers.PrimaryKeyRelatedField(source='activity', queryset=Activity.objects.all())
    userId = serializers.SerializerMethodField()
    optionId = serializers.PrimaryKeyRelatedField(source='option', queryset=Option.objects.all())
    isCorrect = serializers.BooleanField(source='option.correct', read_only=True)

    class Meta:
        model = Response
        fields = ('activityId', 'optionId', 'userId', 'isCorrect')

    def get_userId(self, obj: Response):
        return obj.participant.user.id


class ActivitySerializer(serializers.ModelSerializer):
    options = SerializerMethodField()
    responses = SerializerMethodField()

    class Meta:
        model = Activity
        fields = ('id', 'question', 'options', 'responses')

    def get_options(self, obj):
        return OptionSerializer(obj.options.all(), many=True).data

    def get_responses(self, obj):
        return ResponseSerializer(obj.responses.all(), many=True).data
