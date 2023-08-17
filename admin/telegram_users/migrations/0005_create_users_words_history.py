# Generated by Django 4.2.3 on 2023-08-17 16:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_create_books_sentences'),
        ('telegram_users', '0004_create_users_hero_level_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersWordsHistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_known', models.BooleanField(default=False)),
                ('count_view', models.PositiveIntegerField(default=0)),
                ('correct_answers', models.PositiveIntegerField(default=0)),
                ('incorrect_answers', models.PositiveIntegerField(default=0)),
                ('correct_answers_in_row', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('telegram_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegram_users.telegramusersmodel')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.wordsmodel')),
            ],
            options={
                'verbose_name': "Users' history words",
                'verbose_name_plural': "Users' history words",
                'db_table': 'users_words_history',
            },
        ),
    ]
