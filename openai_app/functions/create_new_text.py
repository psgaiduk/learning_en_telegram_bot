from random import choice

import openai

from settings import settings


def create_new_text(level_id: int) -> str:
    """
    Create new text from chatGPT.

    :return: text.
    """

    openai.api_key = settings.openai_token

    levels = {
        0: {'min_words': 50, 'max_words': 100, 'words': 500, 'authors': ['Милн', 'Кэрролл', 'Поттер', 'Льюис', 'Браун']},
        1: {'min_words': 100, 'max_words': 200, 'words': 1000, 'authors': ['Кинни', 'Риордан', 'Паласио', 'Пилки']},
        2: {'min_words': 200, 'max_words': 300, 'words': 2500, 'authors': ['Чехов', 'Фолкнер', 'Флобер', 'Диккинс', 'Бакман']},
        3: {'min_words': 300, 'max_words': 400, 'words': 5000, 'authors': ['Достоевский', 'Набоков', 'Гюго', 'Толстой', 'Джойс']},
    }

    level = levels.get(level_id)

    text = (
        'Напиши короткий рассказ на английском.',
        f'В рассказе должно быть от {level["min_words"]} до {level["max_words"]} слов из списка ',
        f'{level["words"]} самых распространнённых слов английского языка.',
        f'Рассказ должен быть в стиле писателя {choice(level["authors"])}',
    )

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': '\n'.join(text)}]
    )

    return completion.get('choices', [{}])[0]['message']['content'].replace('\n', '')
