# Generated by Django 4.2.4 on 2023-09-29 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicapp', '0038_remove_payment_amount_remove_payment_appointment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='appointment_date',
            field=models.DateTimeField(null=True),
        ),
    ]
