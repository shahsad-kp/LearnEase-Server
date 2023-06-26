from django.urls import path

from Messages.views import MessageView

urlpatterns = [
    path('<int:classroom_id>/', MessageView.as_view(), name='Messages'),
]
