from db.functions.users import get_all_users
from telegram_messenger_app.core import TelegramSDK


class SendUpdates:

    def __init__(self):
        self._telegram_sdk = TelegramSDK()

    def work(self, text: str, video_link: str):
        all_users = get_all_users()
        for user in all_users:
            self._telegram_sdk.send_video_link(
                telegram_id=user.telegram_id,
                text_message=text,
                video_link=video_link
            )


if __name__ == '__main__':
    text_for_send = '📢 Горячие новости! Мы рады объявить, что обновление нашего телеграмм бота уже доступно для ' \
           'использования! 🚀\n\n' \
           'Теперь вы можете выбрать уровень сложности 🤩 Наш бот теперь имеет 4 уровня сложности 🤯'
    link_to_video = 'BAACAgIAAxkDAAIB42Qga7ECTxBTThed24egCj-h5Z5JAAKVMAAC7cUJSVhjV_YWMpz3LwQ'
    SendUpdates().work(text=text_for_send, video_link=link_to_video)
