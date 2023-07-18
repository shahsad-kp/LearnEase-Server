from rest_framework.fields import ImageField
from rest_framework.serializers import ModelSerializer, CharField

from Users.models import User


class UserSerializer(ModelSerializer):
    profilePicture = ImageField(source='profile_pic', required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'profilePicture']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class UpdateUserSerializer(ModelSerializer):
    profilePicture = ImageField(source='profile_pic', required=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'profilePicture')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profilePicture'] = instance.profile_pic.url
        return representation
