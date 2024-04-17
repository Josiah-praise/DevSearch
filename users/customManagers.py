from django.db.models import Q, Manager
from django.contrib.auth.models import UserManager

class CustomManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        if email is None:
            raise ValueError("Email cannot be null")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields["is_staff"] is not True:
            raise ValueError("is_staff should be set to True")

        if extra_fields["is_superuser"] is not True:
            raise ValueError("is_superuser should be set to True")

        return self._create_user(username, email, password, **extra_fields)


class DeveloperFilter(Manager):
    def search(self, q_string=''):
        query_set = super().all().filter(
            Q(username__icontains=q_string) |
            Q(first_name__icontains=q_string) |
            Q(last_name__icontains=q_string) |
            Q(skill__name__icontains=q_string) |
            Q(short_intro__icontains=q_string) |
            Q(bio__icontains=q_string)
        )
        return query_set