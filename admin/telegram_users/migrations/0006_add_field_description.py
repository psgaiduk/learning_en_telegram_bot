# Generated by Django 4.2.3 on 2023-08-19 16:11

from django.db import migrations, models

from telegram_users.choices import LevelEn, Language
from telegram_users.models import LevelsEnModel, MainLanguagesModel


def add_descriptions(apps, schema_editor):
    LevelsEnModel = apps.get_model('telegram_users', 'LevelsEnModel')
    MainLanguagesModel = apps.get_model('telegram_users', 'MainLanguagesModel')

    for level in LevelsEnModel.objects.all():
        level.description = LevelEn[level.title].description
        level.save()

    for language in MainLanguagesModel.objects.all():
        language.description = Language[language.title].description
        language.save()


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_users', '0005_create_users_words_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='levelsenmodel',
            name='description',
            field=models.CharField(default='test', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mainlanguagesmodel',
            name='description',
            field=models.CharField(default='test', max_length=128),
            preserve_default=False,
        ),
        migrations.RunPython(add_descriptions),
    ]