from openai_app.functions import create_new_text
from db.functions.texts import create_text
from nlp_translate_app.utils import translate_text


def add_new_text_to_db():
    new_en_text = create_new_text()
    text_ru = translate_text(text_on_en=new_en_text, language='ru')
    text_es = translate_text(text_on_en=new_en_text, language='es')
    text_ge = translate_text(text_on_en=new_en_text, language='de')
    text_fr = translate_text(text_on_en=new_en_text, language='fr')
    create_text(text_en=new_en_text, text_ru=text_ru, text_es=text_es, text_fr=text_fr, text_ge=text_ge)
