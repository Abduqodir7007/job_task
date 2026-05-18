from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserLoginSerializer, UserRegistrationSerializer, TokenResponseSerializer, RoleSerializer
from .utils import generate_jwt_token
from .filters import UserFilter
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
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "email": ["iexact", "icontains"],
        "first_name": ["iexact", "icontains"],
        "last_name": ["iexact"],
        "roles__name": ["iexact"],
    }


class UserView(APIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        serializer = UserRegistrationSerializer(request.user)
        return Response(serializer.data)


class RoleListAPIView(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
