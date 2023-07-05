from django.urls import path

from Activities.views import ListActivitiesView

urlpatterns = [
    path('<int:room_id>/', ListActivitiesView.as_view(), name='create-list-activities'),
]
