# Generated by Django 4.2.4 on 2024-03-18 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicapp', '0063_healthmetric_height'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ambulance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=255)),
                ('service_status', models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available', max_length=20)),
                ('vehicle_number', models.CharField(max_length=20)),
                ('vehicle_model', models.CharField(max_length=100)),
                ('vehicle_capacity', models.PositiveIntegerField()),
                ('driver_name', models.CharField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
