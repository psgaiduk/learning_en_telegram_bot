from pathlib import Path

from loguru import logger
from openai import OpenAI

from settings import settings


class AISDK:
    """Класс для работы с OpenAI API."""

    def __init__(self):
        self._client = OpenAI(api_key=settings.ai_token)

    def create_audio_file(self, sentence: str, file_name: str) -> None:
        """
        Создать аудио файл.

        :param sentence: Текст для озвучки.
        :param file_name: имя файла.
        :return: None
        """
        audio_dir = Path.cwd() / "static" / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        speech_file_path = audio_dir / f"{file_name}.mp3"
        logger.debug(f"file path = {speech_file_path}")
        response = self._client.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=sentence,
        )

        response.stream_to_file(speech_file_path)
        logger.debug(f"converted text to audio {response}")
