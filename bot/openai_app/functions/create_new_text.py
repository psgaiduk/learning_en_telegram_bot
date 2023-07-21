from random import choice

import openai

from bot.settings import settings


def create_new_text(level_id: int) -> str:
    """
    Create new text from chatGPT.

    :return: text.
    """

    openai.api_key = settings.openai_token

    levels = {
        0: {
            'min_words': 50,
            'max_words': 100,
            'words': 500,
            'level': 'A1',
            'authors': ['Милн', 'Кэрролл', 'Поттер', 'Льюис', 'Браун']
        },
        1: {
            'min_words': 100,
            'max_words': 200,
            'words': 1000,
            'level': 'A2',
            'authors': ['Кинни', 'Риордан', 'Паласио', 'Пилки']
        },
        2: {
            'min_words': 200,
            'max_words': 300,
            'words': 2500,
            'level': 'B1',
            'authors': ['Чехов', 'Фолкнер', 'Флобер', 'Диккинс', 'Бакман']
        },
        3: {
            'min_words': 300,
            'max_words': 400,
            'words': 5000,
            'level': 'B2',
            'authors': ['Достоевский', 'Набоков', 'Гюго', 'Толстой', 'Джойс']
        },
    }

    level = levels.get(level_id)

    text = (
        'Напиши короткий рассказ на английском.',
        f'В рассказе должно быть от {level["min_words"]} до {level["max_words"]} слов',
        f'Рассаз должен состоять из {level["words"]} самых распространнённых слов английского языка.',
        f'Рассказ должен быть понятен для уровня знания английского {level["level"]}'
        f'Рассказ должен быть в стиле писателя {choice(level["authors"])}',
        f'Учти что рассказ это для обучения, поэтому он обязательно должен быть понятен уровню {level["level"]}'
    )

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': '\n'.join(text)}]
    )

    text_on_en = completion.get('choices', [{}])[0]['message']['content'].replace('\n', '')
    return text_on_en.replace('\n', '').replace('.', '.\n')
