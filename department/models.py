from django.conf import settings
from django.db import models

from base.models import NULLABLE


class Course(models.Model):
    '''Курс'''
    name = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(verbose_name='Картинка', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'Название курса - {self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    '''Урок'''
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)

    name = models.CharField(max_length=100, verbose_name='Название урока')
    preview = models.ImageField(verbose_name='Картинка', **NULLABLE)
    link = models.URLField(verbose_name='Ссылка на видео')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'Название урока - {self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
