from pathlib import Path

from loguru import logger
from openai import OpenAI

from settings import settings


class AISDK:
    """Класс для работы с OpenAI API."""

    def __init__(self):
        self._client = OpenAI(api_key=settings.ai_token)

    def create_audio_file(self, sentence: str, file_name: str, level_order: int, voice: str) -> None:
        """
        Создать аудио файл.
        https://platform.openai.com/docs/guides/text-to-speech

        :param sentence: Текст для озвучки.
        :param file_name: имя файла.
        :param voice: Тип голоса
        :return: None
        """
        audio_dir = Path.cwd() / "static" / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        speed_by_level = [0.7, 0.85, 1, 1, 1.15, 1.3]
        logger.debug(f"level order = {level_order}")
        logger.debug(f"speed = {speed_by_level[level_order - 1]}")

        speech_file_path = audio_dir / f"{file_name}.mp3"
        logger.debug(f"file path = {speech_file_path}")
        response = self._client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=sentence,
            speed=speed_by_level[level_order - 1],
        )

        response.stream_to_file(speech_file_path)
        logger.debug(f"converted text to audio {response}")
