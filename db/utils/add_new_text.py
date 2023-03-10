from openai_app.functions import create_new_text
from db.functions.texts import create_text


def add_new_text_to_db():
    new_text = create_new_text()
    create_text(text=new_text)
    return new_text
