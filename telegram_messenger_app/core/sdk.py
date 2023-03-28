from requests import get, post

from settings import settings


class TelegramSDK:
    """Telegram SDK."""

    _url: str

    def __init__(self) -> None:
        """Init."""

        self._url = f'https://api.telegram.org/bot{settings.telegram_token}'

    def send_video_link(self, telegram_id: int, video_link: str, text_message: str):
        url = self._url + '/sendVideo'

        params_for_send_video = {
            'chat_id': telegram_id,
            'video': video_link,
            'caption': text_message,
        }

        response = get(url, params=params_for_send_video)

    def send_video_file(self):
        url = self._url + '/sendVideo'
        with open('video.mov', 'rb') as f:
            # Отправка POST запроса на сервер Telegram
            response = post(url, data={'chat_id': 232540084}, files={'video': f})
            print(response.json())


if __name__ == '__main__':
    TelegramSDK().send_video_file()

    # TelegramSDK().send_video_link(
    #     telegram_id=232540084,
    #     video_link='BAACAgIAAxkDAAIGcWQgaAqCtddYI-0YWyEFiuFFiWwwAALfMAACukABSUjGI1XQgm8kLwQ',
    #     text_message=text,
    # )
