from django.urls import path

from Users.views import UserRegisterView, UpdateUserView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register-user'),
    path('update/', UpdateUserView.as_view(), name='update-user'),
]
