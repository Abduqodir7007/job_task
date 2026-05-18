from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserLoginView, UserRegistrationView, UserViewSet, UserView, RoleListAPIView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("auth/me/", UserView.as_view(), name="user-detail"),
    path("roles/", RoleListAPIView.as_view(), name="roles-list"),
]
urlpatterns += router.urls