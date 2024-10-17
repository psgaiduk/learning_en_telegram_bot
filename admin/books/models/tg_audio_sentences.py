from django.db.models import (
    AutoField,
    CASCADE,
    TextField,
    ForeignKey,
    Model,
)

from books.models.books_sentences import BooksSentencesModel


class TgAudioSentenceModel(Model):
    """Model of link to audio in telegram."""

    id = AutoField(primary_key=True)
    sentence = ForeignKey(BooksSentencesModel, on_delete=CASCADE, related_name="tg_audio_sentence")
    audio_id = TextField()


    def __str__(self):
        return f"Book {self.sentence.book.title}, Sentence {self.sentence.order}"

    class Meta:
        verbose_name = "TgAudioSentence"
        verbose_name_plural = "TgAudioSentences"
        db_table = "tg_audio_sentences"
