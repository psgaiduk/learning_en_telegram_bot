# Generated by Django 4.2.3 on 2023-07-31 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0004_create_words"),
    ]

    operations = [
        migrations.CreateModel(
            name="BooksSentencesModel",
            fields=[
                ("sentence_id", models.AutoField(primary_key=True, serialize=False)),
                ("order", models.IntegerField()),
                ("text", models.TextField()),
                ("translation", models.JSONField(blank=True, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books_sentences",
                        to="books.booksmodel",
                    ),
                ),
                (
                    "words",
                    models.ManyToManyField(related_name="books_sentences", to="books.wordsmodel"),
                ),
            ],
            options={
                "verbose_name": "Sentence",
                "verbose_name_plural": "Sentences",
                "db_table": "books_sentences",
            },
        ),
    ]
