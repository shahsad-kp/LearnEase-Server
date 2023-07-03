from django.urls import path

from Whiteboard.views import GetWhiteBoardData

urlpatterns = [
    path('<int:room_id>/', GetWhiteBoardData.as_view(), name='Whiteboard')
]
