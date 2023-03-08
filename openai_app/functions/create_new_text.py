from random import choice

import openai

from settings import settings


def create_new_text() -> str:
    """
    Create new text from chatGPT.

    :return: text.
    """
    authors = [
        'Лев Толстой',
        'Владимир Набоков',
        'Фёдор Достевскй',
        'Уильям Фолкнер',
        'Чарльз Диккенс',
        'Антон Чехов',
        'Гюстав Флобер',
        'Джейн Остин',
    ]

    openai.api_key = settings.openai_token

    text = (
        'Напиши короткий рассказ на английском.',
        'В рассказе должно быть не меньше чем 500 слов из списка 5000 самых распространнённых слов английского языка.',
        f'Рассказ должен быть в стиле писателя {choice(authors)}',
        'После каждого предложения добавь литературный перевод на русском языке в квадратных скобках.',
    )

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': '\n'.join(text)}]
    )

    return completion.get('choices', [{}])[0]['message']['content']