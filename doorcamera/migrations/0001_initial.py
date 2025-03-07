# Generated by Django 5.1.2 on 2025-03-05 14:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doorbell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to='guest_images/')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('opened', 'Opened')], default='pending', max_length=10)),
            ],
        ),
    ]
