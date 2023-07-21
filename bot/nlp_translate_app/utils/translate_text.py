from requests import post

from bot.settings import settings


def translate_text(text_on_en: str, language: str) -> str:
    url = 'https://deepl-translator.p.rapidapi.com/translate'

    headers = {
        'content-type': 'application/json',
        'X-RapidAPI-Key': settings.nlp_token,
        'X-RapidAPI-Host': 'deepl-translator.p.rapidapi.com',
    }

    payload = {
        'text': text_on_en,
        'source': 'EN',
        'target': language,
    }

    response = post(url, json=payload, headers=headers).json()

    return response['text']
