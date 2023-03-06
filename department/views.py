import json

import requests
from django.conf import settings

from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from department.models import Course, Lesson, UserSubscription, Payment
from department.permissions import OwnerOrStuff, IsOwner, IsStaff, PermsForViewSetCourse, IsNotStaff
from department.serializers import CourseSerializer, LessonSerializer, UserSubscriptionSerializer, PaymentSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    queryset = UserSubscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [PermsForViewSetCourse]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_anonymous:
            return queryset
        if self.request.user.role == 'moderator':
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    ##### CRUD для модели Lesson при помощи generics


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsStaff]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_anonymous:
            return queryset
        if self.request.user.role == 'moderator':
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsStaff]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsNotStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [OwnerOrStuff]


class LessonRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [OwnerOrStuff]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def post(self, request, *args, **kwargs):
        course_pk = self.kwargs.get('pk')
        course_item = get_object_or_404(Course, pk=course_pk)
        payment, created = Payment.objects.get_or_create(
            course=course_item,
            owner=request.user
        )

        if not created:
            if payment.status_payment =='run':
                return Response(
                {
                    "Статус курса": 'Платеж находится в обработке'
                }
                )
            return Response(
                {
                    "Статус курса": f'Курс {course_item.name} Уже оплачен'
                }
            )


        deta_for_request = {
            "TerminalKey": settings.TERMINAL_KEY,
            "Amount": course_item.price,
            "OrderId": f'{payment.pk}',
            "Description": course_item.name,
            "Receipt": {
                "Email": "a@test.ru",
                "Phone": "+79031234567",
                "EmailCompany": "b@test.ru",
                "Taxation": "osn",
                "Items": [
                    {
                        "Name": course_item.name,
                        "Price": course_item.price,
                        "Quantity": 1.00,
                        "Amount": course_item.price,
                        "PaymentMethod": "full_prepayment",
                        "PaymentObject": "commodity",
                        "Tax": "vat10",
                        "Ean13": "0123456789"
                    }
                ]
            }
        }

        response = requests.post(
            url='https://securepay.tinkoff.ru/v2/Init',
            data=json.dumps(deta_for_request),
            headers={'Content-type': 'application/json'}
        )

        payment_url = response.json()["PaymentURL"]
        payment.payment_url = payment_url
        payment.save()
        return Response(
            {
                "url": payment_url
            }
        )
