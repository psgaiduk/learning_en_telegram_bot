from django.db.models.signals import post_save
from django.dispatch import receiver


from books.models import BooksModel
from books.tasks import create_book_task


@receiver(post_save, sender=BooksModel)
def create_words_and_sentences(sender, instance, created, **kwargs):
    if created:
        create_book_task(instance.book_id)
