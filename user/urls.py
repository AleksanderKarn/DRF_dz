from django.urls import path

from user.views import UserUpdateAPIView, UserListAPIView

urlpatterns = [
    path('update/<int:pk>/', UserUpdateAPIView.as_view()),
    path('list/', UserListAPIView.as_view())
]
