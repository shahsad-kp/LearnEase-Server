from django.urls import path

from Users.views import UserRegisterView, UpdateUserView

urlpatterns = [
    path('update/', UpdateUserView.as_view(), name='update-user'),
]
