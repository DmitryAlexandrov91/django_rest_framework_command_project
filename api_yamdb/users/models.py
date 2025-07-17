"""User model for group project."""
from api.constants import ADMIN, MAX_LENGTH_NAME, MODER, USER
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username

ROLES = (
    (ADMIN, ADMIN),
    (MODER, MODER),
    (USER, USER),
)


class User(AbstractUser):
    """User class for group project."""

    username_validator = validate_username

    email = models.CharField(max_length=MAX_LENGTH_NAME,
                             unique=True,
                             verbose_name='Электронная почта',)
    bio = models.TextField(null=True,
                           blank=True,
                           verbose_name='Биография',)
    role = models.CharField(max_length=max(len(roles[1]) for roles in ROLES),
                            choices=ROLES,
                            default='user',
                            verbose_name='Роль')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        """Return  username."""
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moder(self):
        return self.role == MODER
