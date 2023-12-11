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
                    'content': f'Как опытный учитель английского языка, проанализируйте предложение ученика и выделите идиомы, '
                               f'фразовые глаголы и слова, которые могут быть неизвестны ученику уровня {english_level}. Укажите их тип: '
                               f'идиома - 1, фразовый глагол - 2 или слово - 3. Не нужно переводить слова, добавлять знаки препинаня кроме запятых '
                               f'или артикли. Пример ответа: "once - 3, husband - 3, lived with - 2, burn the midnight oil - 1".'
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
        """
        Создать аудио файл.

        :param sentence: Текст для озвучки.
        :param file_name: имя файла.
        :return: None
        """
        audio_dir = Path.cwd() / 'static' / 'audio'
        audio_dir.mkdir(parents=True, exist_ok=True)

        speech_file_path = audio_dir / f'{file_name}.mp3'
        response = self._client.audio.speech.create(
            model='tts-1',
            voice='shimmer',
            input=sentence,
        )

        response.stream_to_file(speech_file_path)
