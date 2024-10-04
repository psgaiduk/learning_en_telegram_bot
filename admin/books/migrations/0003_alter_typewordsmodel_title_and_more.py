# Generated by Django 4.2.3 on 2023-07-29 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_create_model_type_words"),
    ]

    operations = [
        migrations.AlterField(
            model_name="typewordsmodel",
            name="title",
            field=models.CharField(
                choices=[
                    ("word", "Word"),
                    ("phrase_verb", "Phrase verb"),
                    ("idiomatic_expression", "Idiomatic expression"),
                ],
                max_length=128,
            ),
        ),
        migrations.AlterField(
            model_name="typewordsmodel",
            name="type_word_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
