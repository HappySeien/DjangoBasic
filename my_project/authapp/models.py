from django.db import models
from django.contrib.auth.models import AbstractUser

from settingsapp.models import NULLABLE
from authapp.services.user_avatars_path import users_avatars_path

# Create your models here.


class User(AbstractUser):
    """
    Модель пользователя сайта
    """

    email = models.EmailField(blank=True, unique=True, verbose_name='Email')
    age = models.PositiveBigIntegerField(**NULLABLE, verbose_name='Возраст')
    avatar = models.ImageField(upload_to=users_avatars_path, **NULLABLE)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
