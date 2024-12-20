# Generated by Django 4.2.3 on 2024-11-12 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_add_numerals'),
    ]

    operations = [
        migrations.CreateModel(
            name='TgAudioSentenceModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('audio_id', models.TextField()),
                ('sentence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tg_audio_sentence', to='books.bookssentencesmodel')),
            ],
            options={
                'verbose_name': 'TgAudioSentence',
                'verbose_name_plural': 'TgAudioSentences',
                'db_table': 'tg_audio_sentences',
            },
        ),
    ]
