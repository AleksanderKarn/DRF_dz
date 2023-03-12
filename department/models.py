from django.conf import settings
from django.db import models

from base.models import NULLABLE
from user.models import User


class Course(models.Model):
    '''Курс'''
    name = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(verbose_name='Картинка', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(default=1000)

    def __str__(self):
        return f'Курс - {self.name}'

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


class UserSubscription(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Подписка на курс')

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'Подписка для {self.owner}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Payment(models.Model):
    RUN = "run"
    REJECT = 'reject'
    EXECUTED = 'executed'
    PROCESSED = 'processed'  # Статус после отправленного письма о том что платеж выполнен
    STATUS_PAYMENT = (
        ('reject', 'отклонен'),
        ('run', 'в обработке'),
        ('executed', 'выполнен'),
        ('processed', 'обработан')
    )
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='payment_course',
                               verbose_name='Подписка на курс', null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payment_owner', on_delete=models.SET_NULL,
                              null=True)
    payment_url = models.CharField(max_length=250, verbose_name='Описание заказа')

    status_payment = models.CharField(choices=STATUS_PAYMENT, max_length=10, default=RUN, verbose_name='Статус платежа')

    terminal_key = models.CharField(max_length=50, verbose_name='TerminalKey', **NULLABLE)
    payment_id = models.CharField(max_length=20, verbose_name='PaymentId', **NULLABLE)
    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)