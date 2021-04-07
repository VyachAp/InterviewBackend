from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField("Номер телефона", unique=True)
    first_name = models.CharField("Имя", max_length=30, blank=True)
    last_name = models.CharField("Фамилия", max_length=30, blank=True)
    date_joined = models.DateTimeField("Дата регистрации", auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = [
        "phone",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
