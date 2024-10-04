from http import HTTPStatus
from typing import Optional

from requests import get

from settings import settings


def translate_text(text_on_en: str, language: str) -> Optional[str]:
    url = "https://nlp-translation.p.rapidapi.com/v1/translate"

    payload = {
        "text": text_on_en,
        "from": "en",
        "to": language,
    }

    headers = {
        "X-RapidAPI-Key": settings.nlp_token,
        "X-RapidAPI-Host": "nlp-translation.p.rapidapi.com",
    }

    response = get(url, params=payload, headers=headers)

    if response.status_code != HTTPStatus.OK:
        return ""

    return response.json()["translated_text"][language]
