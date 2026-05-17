from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from config.constants import Constants
from .models import User
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "role")
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"required": True},
        }

    def validate_role(self, value):
        if value == Constants.UserRoles.ADMIN:
            raise serializers.ValidationError(_("Admin role cannot be assigned during registration."))
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Email is already in use."))
        return value

    def validate_password(self, value):
        user = self.context.get("request").user if self.context.get("request") else None
        validate_password(value, user)
        return value

    def validate_first_name(self, value):
        if not all(ch.isalpha() for ch in value):
            raise serializers.ValidationError(_("First name must contain letters only."))
        return value

    def validate_last_name(self, value):
        if not all(ch.isalpha() for ch in value):
            raise serializers.ValidationError(_("Last name must contain letters only."))
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            email=attrs["email"],
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError(_("Invalid email or password."))

        attrs["user"] = user
        return attrs
