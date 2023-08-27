from django.contrib.auth.tokens import default_token_generator
from rest_framework.fields import ImageField
from rest_framework.serializers import ModelSerializer, BooleanField

from Auth.models import EmailVerification
from Users.models import User


class UserSerializer(ModelSerializer):
    profilePicture = ImageField(source='profile_pic', required=False)
    isVerified = BooleanField(source='is_verified', required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'profilePicture', 'isVerified']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class UpdateUserSerializer(ModelSerializer):
    profilePicture = ImageField(source='profile_pic', required=False)
    isVerified = BooleanField(source='is_verified', required=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'profilePicture', 'isVerified')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profilePicture'] = instance.profile_pic.url
        return representation

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        if 'email' in validated_data and instance.email != validated_data['email']:
            instance.is_verified = False
            instance.save()
            token = default_token_generator.make_token(instance)
            EmailVerification.objects.create(email=instance.email, token=token, user=instance).send()

        return instance
