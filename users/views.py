from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend


from config.constants import Constants
from payments.permissions import IsAdminRole
from .serializers import (
    RoleSerializer,
    TokenResponseSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserDashboardSerializer,
    UserResponseSerializer,
)
from .utils import generate_jwt_token
from .models import Role

User = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = generate_jwt_token(user)
        return Response(token, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token = generate_jwt_token(serializer.validated_data["user"])
        return Response(token, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    permission_classes = [IsAdminRole]
    queryset = User.objects.all()
    serializer_class = UserResponseSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "email": ["iexact", "icontains"],
        "first_name": ["iexact", "icontains"],
        "last_name": ["iexact"],
        "roles__name": ["iexact"],
    }

    @action(detail=False, methods=["get"], permission_classes=[IsAdminRole])
    def dashboard(self, request):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        admin_users = User.objects.filter(roles__name=Constants.UserRoles.ADMIN).count()
        payment_users = User.objects.filter(roles__name=Constants.UserRoles.PAYMENT).count()
        report_users = User.objects.filter(roles__name=Constants.UserRoles.REPORTS).count()

        data = {
            "total_users": total_users,
            "active_users": active_users,
            "admin_users": admin_users,
            "payment_users": payment_users,
            "report_users": report_users,
        }
        
        serializer = UserDashboardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):
    serializer_class = UserResponseSerializer

    def get(self, request):
        serializer = UserResponseSerializer(request.user)
        return Response(serializer.data)


class RoleListAPIView(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
