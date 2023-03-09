from openai_app.functions import create_new_text
from db.functions.texts import create_text

new_text = create_new_text()
create_text(text=new_text)
