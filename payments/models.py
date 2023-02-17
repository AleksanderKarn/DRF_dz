from django.db import models

from base.models import NULLABLE
from department.models import Course
from user.models import User


class Payment(models.Model):
    CASH = 'cash'
    CARD = 'card'
    PAYMENTS = (
        ('cash', 'наличными'),
        ('card', 'картой')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',**NULLABLE)
    course_pay = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)

    date_pay = models.DateField(auto_now_add=True)
    price = models.FloatField(default=0, verbose_name='Цена покупки')
    payment_method = models.CharField(choices=PAYMENTS, default=CARD,
                                      max_length=20, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.course_pay} для  {self.user} за  {self.price}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'