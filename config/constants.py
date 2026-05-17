"""Project-wide constants."""
from django.utils.translation import gettext_lazy as _


class Constants:
    class Validation:
        NAME_REGEX = r"^[A-Za-z]+$"
        PASSWORD_SPECIAL_CHARACTERS = "!@#$%^&"

    class UserRoles:
        """Constants for user roles."""
        ADMIN = 'admin'
        USER = 'user'
        MODERATOR = 'moderator'

        CHOICES = (
            (ADMIN, _('Admin')),
            (USER, _('User')),
            (MODERATOR, _('Moderator')),
        )