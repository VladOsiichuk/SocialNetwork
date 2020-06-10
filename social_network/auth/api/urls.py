from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from social_network.auth.api.views import UserRegisterAPIView, UserLoginAPIView

token_urlpatterns = [
    path("login/", UserLoginAPIView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view()),
    path("token/", include(token_urlpatterns)),
]
