from requests import get
from nltk.text import sent_tokenize

from settings import settings


def translate_text(text_on_en: str, language: str) -> str:
    MAX_LETTERS = 800
    url = 'https://nlp-translation.p.rapidapi.com/v1/translate'
    headers = {
        'X-RapidAPI-Key': settings.nlp_token,
        'X-RapidAPI-Host': 'nlp-translation.p.rapidapi.com'
    }

    translate = []
    text_on_en = text_on_en.replace('\n', '').replace('.', '. ')
    sentences_en = sent_tokenize(text=text_on_en, language='english')
    part_text_for_translate = ''

    for sentence in sentences_en:
        if len(part_text_for_translate + sentence) > MAX_LETTERS:
            params_for_translate = {
                'text': part_text_for_translate,
                'to': language,
                'from': 'en',
            }
            response = get(url=url, params=params_for_translate, headers=headers).json()
            translate.append(response.get('translated_text', {}).get(language))
            part_text_for_translate = ''
        else:
            part_text_for_translate += sentence

    return ''.join(translate)
