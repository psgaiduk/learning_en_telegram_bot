from http import HTTPStatus
from typing import Optional

from requests import get

from settings import settings


def translate_word(word: str, language: str) -> Optional[str]:
    url = 'https://just-translated.p.rapidapi.com/'

    headers = {
        "X-RapidAPI-Key": settings.translate_word_token,
        "X-RapidAPI-Host": "just-translated.p.rapidapi.com"
    }

    querystring = {'lang': language, 'text': word}

    response = get(url, headers=headers, params=querystring)
    if response.status_code != HTTPStatus.OK:
        return ''

    return ', '.join(response.json()['text'])
