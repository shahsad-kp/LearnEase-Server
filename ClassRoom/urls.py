from django.urls import path

from ClassRoom.views import CreateClassRoom, GetTopics, GetClassRoom, GetHistory

urlpatterns = [
    path('create/', CreateClassRoom.as_view(), name='CreateClassRoom'),
    path('<int:classroom_id>/', GetClassRoom.as_view(), name='GetTopics'),
    path('topics/<int:classroom_id>/', GetTopics.as_view(), name='GetTopics'),
    path('history/', GetHistory.as_view(), name='GetHistory'),
]
