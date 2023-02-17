# Generated by Django 4.1.7 on 2023-02-17 15:38

from django.db import migrations

def add_payments_in_bd(apps, schema_editor):
    Payment = apps.get_model('payments', 'Payment')
    count = 1
    for i in range(5):
        Payment.objects.create(price=int(f'{count}00000'))
        count += 1



class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_payment_course_pay_alter_payment_user'),
    ]

    operations = [
        migrations.RunPython(add_payments_in_bd)
    ]
