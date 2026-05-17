from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserLoginSerializer, UserRegistrationSerializer, TokenResponseSerializer
from .utils import generate_jwt_token
from drf_spectacular.utils import extend_schema
@extend_schema(
    responses=TokenResponseSerializer,
)
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
