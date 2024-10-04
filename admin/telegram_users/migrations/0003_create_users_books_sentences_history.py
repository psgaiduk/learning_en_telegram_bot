# Generated by Django 4.2.3 on 2023-08-16 16:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0005_create_books_sentences"),
        ("telegram_users", "0002_create_users_books_history"),
    ]

    operations = [
        migrations.CreateModel(
            name="UsersBooksSentencesHistoryModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("check_words", models.JSONField(blank=True, null=True)),
                ("is_read", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(default=datetime.datetime.utcnow)),
                (
                    "sentence",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="books.bookssentencesmodel",
                    ),
                ),
                (
                    "telegram_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="telegram_users.telegramusersmodel",
                    ),
                ),
            ],
            options={
                "verbose_name": "User's books sentences history",
                "verbose_name_plural": "Users' books sentences history",
                "db_table": "users_books_sentences_history",
            },
        ),
    ]
