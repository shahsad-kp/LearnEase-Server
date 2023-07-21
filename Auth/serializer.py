from rest_framework.serializers import ModelSerializer 

from .models import EmailOtpVerification

class OTPSerializer(ModelSerializer):
    class Meta:
        model = EmailOtpVerification
        fields = ('id', 'email', 'expired_at')
        
    def create(self, validated_data):
        # create otp``
        return super().create(validated_data)