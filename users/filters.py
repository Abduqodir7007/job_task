from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    roles = filters.CharFilter(field_name="roles__name", lookup_expr="iexact")

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "roles"]
