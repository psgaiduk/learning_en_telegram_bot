# Generated by Django 4.2.3 on 2023-12-14 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0005_create_books_sentences"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookssentencesmodel",
            name="description_time",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bookssentencesmodel",
            name="sentence_times",
            field=models.TextField(blank=True, null=True),
        ),
    ]
