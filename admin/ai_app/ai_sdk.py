from pathlib import Path

from openai import OpenAI

from settings import settings


class AISDK:
    """Класс для работы с OpenAI API."""

    def __init__(self):
        self._client = OpenAI(api_key=settings.ai_token)

    def get_words(self, sentence: str, english_level: str) -> list[str]:
        """
        Получить слова из предложения.

        :param sentence: предложение.
        :param english_level: уровень английского.
        :return: список слов.
        """

        response = self._client.chat.completions.create(
            model='gpt-4',
            messages=[
                {
                    "role": 'assistant',
                    'content': f'Как учитель английского языка с 30-летним опытом, проанализируйте следующее предложение ученика и выделите '
                               f'все идиомы, фразовые  глаголы и сложные слова, которые может не знать ученик уровня {english_level}. указав их '
                               f'через запятую. Перевод слов не нужен. Добавь для слов их тип через дефис (-). Для идиом - 1, '
                               f'для фразовых глаголов - 2. для сложных одиночных слов - 3. Обязательно после дефиса добавь пробел. Не надо'
                               f'добавлять слова в скобках и в конце точку. Дополнительно не надо ничего писать, вот примерный формат ответа: '
                               f'once - 3, husband - 3, small - 3, garden - 3, lived with - 2, burn the midnight oil - 1'
                },
                {
                    'role': 'user',
                    'content': sentence,
                },
            ],
        )

        words = response.choices[0].message.content.lower()

        if '.' in words:
            words.replace('.', '')

        return words.split(', ')

    def create_audio_file(self, sentence: str, file_name: str) -> None:
        speech_file_path = Path(__file__).parent / f"{file_name}.mp3"
        response = self._client.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=sentence,
        )

        response.stream_to_file(speech_file_path)
