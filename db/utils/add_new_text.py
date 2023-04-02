from loguru import logger

from openai_app.functions import create_new_text
from db.functions.texts import create_text
from nlp_translate_app.utils import translate_text


def add_new_text_to_db():
    logger.info('start add new text')
    for level_id in range(4):
        new_en_text = create_new_text(level_id=level_id)
        text_ru = translate_text(text_on_en=new_en_text, language='RU')
        text_es = translate_text(text_on_en=new_en_text, language='ES')
        text_fr = translate_text(text_on_en=new_en_text, language='FR')
        text_ge = translate_text(text_on_en=new_en_text, language='DE')

        create_text(
            text_en=new_en_text,
            text_ru=text_ru,
            text_es=text_es,
            text_fr=text_fr,
            text_ge=text_ge,
            level=level_id,
        )


if __name__ == '__main__':
    add_new_text_to_db()
