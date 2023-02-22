from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import UserUpdateAPIView, UserListAPIView, UserCreateAPIView

urlpatterns = [
    path('update/<int:pk>/', UserUpdateAPIView.as_view()),
    path('create/', UserCreateAPIView.as_view()),
    path('list/', UserListAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
