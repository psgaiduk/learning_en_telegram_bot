from requests import get

from settings import settings


def translate_text(text_on_en: str, language: str) -> str:
    MAX_LETTERS = 990
    url = 'https://nlp-translation.p.rapidapi.com/v1/translate'
    headers = {
        'X-RapidAPI-Key': settings.nlp_token,
        'X-RapidAPI-Host': 'nlp-translation.p.rapidapi.com'
    }

    translate = []
    text_on_en = text_on_en.replace('\n', '')

    for start_symbol in range(0, len(text_on_en), MAX_LETTERS):
        part_of_text = text_on_en[start_symbol:start_symbol + MAX_LETTERS]

        params_for_translate = {
            'text': part_of_text,
            'to': language,
            'from': 'en',
        }
        response = get(url=url, params=params_for_translate, headers=headers).json()
        translate.append(response.get('translated_text', {}).get(language))

    return ''.join(translate)

