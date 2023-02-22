from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from payments.models import Payment
from payments.serializers import PaymentSerializer
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    count_payments = serializers.SerializerMethodField()
    list_payments = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'country',
            'first_name',
            'last_name',
            'list_payments',
            'count_payments',
        )

    def validate_password(self, value: str) -> str:
        return make_password(value)

    def get_count_payments(self, instance):
        count_payments = Payment.objects.filter(user_id=instance).count()
        return count_payments
