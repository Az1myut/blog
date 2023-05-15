from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager
from . import constants as user_constants


class User(AbstractUser):
    username = None # Удаляем username field, потому-что, 
    # мы используем email как идентификатор пользователя
    email = models.EmailField(
        verbose_name=_("email"), unique=True, null=True, db_index=True
    )
    is_active = models.BooleanField(verbose_name=_("Активен"), default=False)
    is_staff = models.BooleanField(verbose_name=_("Сотрудник"), default=False)
    date_joined = models.DateTimeField(
        verbose_name=_("Дата регистрации"), default=timezone.now
    )
    user_type = models.PositiveSmallIntegerField(
        verbose_name=_("Тип пользователя"), choices=user_constants.USER_TYPE_CHOICES
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = UserManager()


    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(
        verbose_name=_("Пользователь"),
        to=User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="user_profile",
    )
    phone = models.CharField(
        verbose_name=_("Телефон"), max_length=255, blank=True, null=True
    )
    is_verified = models.BooleanField(verbose_name=_("Проверен"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.email}"
