from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from Activities.models import Activity
from Activities.serializers import ActivitySerializer


class ListActivitiesView(ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(room_id=self.kwargs['room_id'])
