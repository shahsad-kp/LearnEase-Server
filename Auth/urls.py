from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Auth.views import LoginView, UserRegisterView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login-user'),
    path('register/', UserRegisterView.as_view(), name='register-user'),
]
