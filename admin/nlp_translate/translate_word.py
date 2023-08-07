from http import HTTPStatus
from typing import Optional

from requests import post

from settings import settings


def translate_word(word: str, language: str) -> Optional[str]:
    url = 'https://deep-translate1.p.rapidapi.com/language/translate/v2'

    payload = {
        'q': word,
        'source': 'en',
        'target': language,
    }

    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': settings.translate_word_token,
        'X-RapidAPI-Host': 'deep-translate1.p.rapidapi.com'
    }

    response = post(url, json=payload, headers=headers)

    if response.status_code != HTTPStatus.OK:
        return ''

    return response.json()['data']['translations']['translatedText']
