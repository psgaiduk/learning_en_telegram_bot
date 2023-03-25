from openai_app.functions import create_new_text
from db.functions.texts import create_text
from nlp_translate_app.utils import translate_text


def add_new_text_to_db():
    for level_id in range(4):
        new_en_text = create_new_text(level_id=level_id)
        text_ru, text_en = translate_text(text_on_en=new_en_text, language='RU')
        create_text(text_en=text_en, text_ru=text_ru, text_es='', text_fr='', text_ge='', level=level_id)
