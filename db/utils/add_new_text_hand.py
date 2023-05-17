from loguru import logger

from db.functions.texts import create_text
from nlp_translate_app.utils import translate_text


def add_new_text_to_db(new_en_text: str, level: int) -> None:
    """
    Add new text to db.

    :param new_en_text: new text on english
    :param level: level of text
    :return: None
    """
    logger.info('start add new text')

    new_en_text = new_en_text.replace("/", "*")

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
        level=level,
    )


if __name__ == '__main__':
    text = """"Tom is a boy.
He is ten years old.
Tom lives in New York.
New York is a big city.
Tom likes to ride his bike.
He rides his bike to school.
School starts at nine o'clock.
Tom's teacher is Mr. Smith.
Mr. Smith is nice.
Tom's best friend is Jerry.
Jerry also rides a bike to school.
After school, they do their homework together.
Then they play basketball.
Basketball is their favorite sport.
On weekends, Tom visits the /zoo/.
The zoo is big.
It has many animals.
Tom's favorite animal is the tiger.
He likes to draw tigers.
Tom's mother is a doctor.
His father is a policeman.
Tom has a sister.
Her name is Mary.
Mary is a baby.
Tom loves his family.
He is happy in New York."""

    add_new_text_to_db(new_en_text=text, level=0)
