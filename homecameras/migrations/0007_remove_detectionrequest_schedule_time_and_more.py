# Generated by Django 5.1.2 on 2025-02-20 08:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homecameras', '0006_detectionrequest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detectionrequest',
            name='schedule_time',
        ),
        migrations.AddField(
            model_name='detectionrequest',
            name='name',
            field=models.CharField(default='User Schedules', max_length=255),
        ),
        migrations.AlterField(
            model_name='detectionrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
