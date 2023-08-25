from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from Auth.models import EmailVerification
from Users.models import User
from Users.serializers import UserSerializer


class LoginView(APIView):
    """
    View for logging in a user.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            error = {}
            if email is None:
                error['email'] = ['This field is required.']
            if password is None:
                error['password'] = ['This field is required.']
            return Response(error, status=HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if not user:
            return Response({"detail": "No active account found with the given credentials"},
                            status=HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
        return Response(data, status=HTTP_200_OK)


class UserRegisterView(CreateAPIView):
    """
    View for registering a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 201:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
            user = User.objects.get(email=serializer.data['email'])
            token = default_token_generator.make_token(user)
            EmailVerification.objects.create(email=user.email, token=token, user=user).send()

            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
            response.data = data
        return response


class VerifyEmailView(APIView):
    """
    View for verifying a user's email.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        if request.user.is_verified:
            return Response({'detail': 'Email already verified.'}, status=HTTP_400_BAD_REQUEST)
        try:
            email_verification = EmailVerification.objects.get(token=token)
            user = request.user
            if user != email_verification.user:
                return Response({'detail': 'Invalid token.'}, status=HTTP_400_BAD_REQUEST)
            user.is_verified = True
            user.save()
            email_verification.delete()
            return Response({'detail': 'Email successfully verified.'}, status=HTTP_200_OK)
        except EmailVerification.DoesNotExist:
            return Response({'detail': 'Invalid token.'}, status=HTTP_400_BAD_REQUEST)
