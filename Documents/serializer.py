from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from Documents.models import Document


class DocumentSerializer(ModelSerializer):

    class Meta:
        model = Document
        fields = ('id', 'docfile', 'title')

    # def create(self, validated_data):
    #     validated_data['room_id'] = self.context['view'].kwargs['room_id']
    #     return super().create(validated_data)
