from django.urls import path

from Documents.views import DocumentCreateAPIView

urlpatterns = [
    path('<int:room_id>/', DocumentCreateAPIView.as_view(), name='documents'),
]
