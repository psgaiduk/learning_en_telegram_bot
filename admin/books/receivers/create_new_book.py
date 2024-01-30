from django.db.models.signals import post_save
from django.dispatch import receiver


from books.models import BooksModel
from books.tasks import create_book_task


@receiver(post_save, sender=BooksModel)
def create_words_and_sentences(sender, instance, created, **kwargs):
    """
    Signal Receiver: post_save, sender=BooksModel

    Method that serves as a signal receiver for the post_save signal. This method is triggered whenever an instance of
    the BooksModel is saved. It takes in the following parameters:

    - sender: The sender of the signal.
    - instance: The instance of the BooksModel that was saved.
    - created: A boolean flag indicating whether the instance was created or updated.
    - **kwargs: Additional keyword arguments that may be passed along with the signal.
    """
    create_book_task(instance.book_id)
