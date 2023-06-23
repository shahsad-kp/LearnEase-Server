from rest_framework.serializers import ModelSerializer

from Users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'profile_pic']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
