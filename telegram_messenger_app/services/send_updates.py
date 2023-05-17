from db.functions.users import get_all_users
from telegram_messenger_app.core import TelegramSDK


class SendUpdates:

    def __init__(self):
        self._telegram_sdk = TelegramSDK()

    def work(self, text: str, video_link: str):
        all_users = get_all_users()
        for user in all_users:
            self._telegram_sdk.send_message(
                telegram_id=user.telegram_id,
                message=text,
            )


if __name__ == '__main__':
    text_for_send = 'Привет, языковые викинги! ⚔️🎉\n\n' \
                    'У нас тут обнова прошла! Теперь уровни сложности текстов в нашем боте стали точно такими, ' \
                    'какими они должны быть: например теперь "легкий" уровень у нас - это как пикник на свежем ' \
                    'воздухе, просто и приятно! 🌳🌼 🌳🏔️\n\n' \
                    'И у нас есть ещё один козырь в рукаве: теперь в текстах будут переводы сложных слов! 🧩🔍 ' \
                    'Так что чтение и изучение станут для вас как уютный вечер с любимым фильмом - ' \
                    'расслабляющим и увлекательным. 🎬🍿\n\n'

    link_to_video = 'BAACAgIAAxkDAAIB42Qga7ECTxBTThed24egCj-h5Z5JAAKVMAAC7cUJSVhjV_YWMpz3LwQ'
    SendUpdates().work(text=text_for_send, video_link=link_to_video)
