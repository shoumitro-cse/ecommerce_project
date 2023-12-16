from django.urls import path
from .views import UserRegisterAPIView, UserLoginAPIView, UserLogoutAPIView


urlpatterns = [
    path('user/register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('user/login/', UserLoginAPIView.as_view(), name='user-login'),
    path('user/logout/', UserLogoutAPIView.as_view(), name='user-logout'),
]

