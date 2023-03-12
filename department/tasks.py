import json

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import requests
from DRF_1.celery import app
from department.models import UserSubscription, Course, Payment
from user.models import User

MESSAGE = {
    "update_cource": 'Ваш курс был недавно обновлен!',
    "status_payment": 'Оплата курса прошла успешно!'
}


def send_mailing(course_pk, message=MESSAGE["update_cource"]):
    '''
    функция собирает айдишники подписчиков указанных в рассылке
    собирает в список их емайлы и производит рассылку на основании полученных данных
    :param mailing:
    :return:
    '''

    owner_ids = UserSubscription.objects.all().filter(courses_id=course_pk)
    _id = []
    for ids in owner_ids:
        _id.append(ids.owner_id)
    subscribers = User.objects.all().filter(id__in=_id)
    subscriber_email = []
    for subscriber in subscribers:
        subscriber_email.append(subscriber.email)

    send_mail(
        subject="Уведомление",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=subscriber_email
    )


@shared_task
def course_check(course_pk):
    send_mailing(course_pk, message=MESSAGE["update_cource"])


@app.task
def pay_check():
    filter_cond = {"status_payment": "executed"}
    payment_list = Payment.objects.filter(**filter_cond)
    if payment_list.exists():
        for course in payment_list:
            course_pk = course.course_id
            send_mailing(course_pk, message=MESSAGE["status_payment"])
        for payment in payment_list:
            payment.status_payment = "processed"
            payment.save()

@app.task
def status_check():
    filter_cond = {"status_payment": "run"}
    payment_list = Payment.objects.filter(**filter_cond)
    if payment_list.exists():
        for payment in payment_list:

            deta_for_request = {
                "TerminalKey": settings.TERMINAL_KEY,
                "PaymentId": payment.payment_id,
                "Token": payment.token
            }
            response = requests.post(
                url='https://securepay.tinkoff.ru/v2/GetState',
                data=json.dumps(deta_for_request),
                headers={'Content-type': 'application/json'}
            )
            success_pay = response.json()["Success"]
            if success_pay == True:
                payment.status_payment = "executed"
                payment.save()
            elif success_pay == False:
                payment.status_payment = "reject"
                payment.save()


# команды для запуска CELERY и BEET

# celery -A DRF_1 worker -l INFO -P eventlet

# celery -A DRF_1 beat -l info -S django
