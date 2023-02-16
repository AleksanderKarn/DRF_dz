from django.contrib.auth.models import AbstractUser
from django.db import models

from base.models import NULLABLE


class User(AbstractUser):
    '''Пользователь'''
    verify_token = models.CharField(**NULLABLE, max_length=35, verbose_name='Токен верификации')
    verify_token_expired = models.DateTimeField(**NULLABLE, verbose_name='Дата истечения токена')

    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)

    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    country = models.CharField(verbose_name='Страна', max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'Пользователь {self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
