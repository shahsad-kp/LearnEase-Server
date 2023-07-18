from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from Users.models import User
from Users.serializers import UserSerializer, UpdateUserSerializer


class UpdateUserView(UpdateAPIView):
    """
    View for updating a new user.
    """
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        return response
