from django.urls import path
from rest_framework import routers
from .views import UserListApiView, LoginAPIView, LogoutAPIView

router = routers.DefaultRouter()

# specify URL Path for rest_framework
urlpatterns = [
    # path("", include(router.urls)),
    path('userdetali/', UserListApiView.as_view(), name='user_list'),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
