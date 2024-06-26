# Generated by Django 5.0.6 on 2024-05-16 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScanResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=100)),
                ('app_name', models.CharField(max_length=100)),
                ('is_safe', models.BooleanField(default=True)),
                ('scan_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
