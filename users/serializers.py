from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from config.constants import Constants
from .models import User, Role
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        many=True,
        required=True,
        allow_empty=False,
    )

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "roles")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Email is already in use."))
        return value

    def validate_roles(self, value):
        # value is a list of Role instances

        for role in value:
            if role.name == Constants.UserRoles.ADMIN:
                raise serializers.ValidationError(_("Admin role cannot be assigned during registration."))
        return value

    def validate_password(self, value):
        special_characters = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        if not any(ch in special_characters for ch in value):
            raise serializers.ValidationError(_("Password must contain at least one special character."))

        user = self.context.get("request").user if self.context.get("request") else None
        validate_password(value, user)  # additional validation, built-in validators
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
        roles = validated_data.pop("roles", [])
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        user_role = Role.objects.filter(name=Constants.UserRoles.USER).first()

        if roles:
            user.roles.set(roles)
        else:
            user.roles.add(user_role)  # default role is user role
        return user


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model."""

    display = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ("id", "name", "display")

    def get_display(self, obj):
        return obj.get_name_display()


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")


class UserResponseSerializer(serializers.ModelSerializer):
    roles = UserRoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "roles")


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


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")

class UserDashboardSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    admin_users = serializers.IntegerField()
    payment_users = serializers.IntegerField()
    report_users = serializers.IntegerField()