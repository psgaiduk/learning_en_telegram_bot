from django.core.management.base import BaseCommand

from books.processes import AddNewWordsProcess
from telegram_users.choices import Language


class Command(BaseCommand):
    help = "Add new words to the database."

    def __init__(self) -> None:
        """Init."""
        super().__init__()
        self._add_new_words_process = AddNewWordsProcess()

    def add_arguments(self, parser) -> None:
        """
        Add arguments to the command line.

        :param parser: Command line
        """
        parser.add_argument("words", type=str)
        parser.add_argument("type_words", type=str)

    def handle(self, *args, **options) -> None:
        """
        Handle the command to add new words to the database.

        :param args: Command line arguments.
        :param options: Command line keyword arguments.
        """
        words = []
        words_list = options.get("words").split("\n")
        for word in words_list:
            word = word.replace(" - ", "***").replace('"', "")
            word_with_translate = word.split("***")
            word_dict = {"word": word_with_translate.pop(0), "translate": {}}
            for index, language in enumerate(Language.choices()):
                word_translate = word_with_translate[index]
                word_dict["translate"][language[0]] = word_translate
            words.append(word_dict)

        self._add_new_words_process(words=words, type_words=options.get("type_words"))
