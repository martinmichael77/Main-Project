# Generated by Django 4.2.4 on 2024-02-06 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicapp', '0045_counselor_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('contact', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('latitude', models.CharField(blank=True, max_length=20, null=True)),
                ('longitude', models.CharField(blank=True, max_length=20, null=True)),
                ('opening_time', models.TimeField(blank=True, null=True)),
                ('closing_time', models.TimeField(blank=True, null=True)),
                ('opening_days', models.CharField(blank=True, max_length=100, null=True)),
                ('hospital_image', models.ImageField(blank=True, null=True, upload_to='hospital_images/')),
                ('avgrating', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
