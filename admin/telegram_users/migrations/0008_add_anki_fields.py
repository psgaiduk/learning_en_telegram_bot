# Generated by Django 4.2.3 on 2024-03-23 04:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_users', '0007_userreferralsmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='userswordshistorymodel',
            name='increase_factor',
            field=models.FloatField(default=2.0),
        ),
        migrations.AddField(
            model_name='userswordshistorymodel',
            name='interval_repeat',
            field=models.PositiveIntegerField(default=600),
        ),
        migrations.AddField(
            model_name='userswordshistorymodel',
            name='repeat_datetime',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
    ]
