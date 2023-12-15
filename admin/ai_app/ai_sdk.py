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

    def translate_and_analyse(self, text: str) -> str:
        """
        Translate text and analysis.

        :param text: text.
        :return: text with translate and analysis.
        """

        prompt = ('You are an English teacher with 30 years of experience.\n'
                  'The student will send you a text.\n'
                  'Break it down into sentences\n'
                  'You must translate each part into Russian.\n'
                  'And for each part, you must provide compound words (it must be one word), phrasal verbs (such as bring up, put up with and others)'
                  ' and idioms that the student may not know at the Beginner level.\n'
                  'You also need to write what time the sentence refers to, consider each sentence as a separate text, if there are two different '
                  'times in the sentence, then indicate them separated by a comma.\n'
                  'Additionally, perform an analysis of time in a sentence in Russian. Determine why this tense is used and focus on '
                  'word markers if they exist.\n'
                  'Don\'t add anything extra\n'
                  'This is how it should look,'
                  'The student gives you the text:\n'
                  'At first, it was small and weak, but she watered it and told it stories, and over the years, '
                  'it got bigger and bigger. Finally, the turnip was giant!\n'
                  'And this is your answer:\n'
                  'At first, it was small and weak, but she watered it and told it stories, and over the years, it got bigger and bigger.  '
                  '--- Сначала он был маленьким и слабым, но она поливала его и рассказывала ему истории, и с годами он становился все больше '
                  'и больше. --- at first: сначала, watered: поливал, told: сказал,  stories: истории, and over the years: и с годами, '
                  'it got bigger: стал больше -- Past Simple --- Past Simple используется здесь, потому что предложение описывает завершенное '
                  'действие или состояние в прошлом. Признаки: использование формы "was" для глагола "to be" для описания прошлого.\n\n'
                  'Finally, the turnip was  giant! --- Наконец-то репа оказалась гигантской! '
                  '--- finally: окончательно, turnip: репа, was: был, giant: гигант. --- Past Simple --- Past Simple используется здесь, '
                  'потому что предложение описывает завершенное действие или состояние в прошлом. Признаки: использование формы "was" для '
                  'глагола "to be" для описания прошлого.\n'
                  'Strictly follow this answer format, no need to add anything extra.'
                  )

        response = self._client.chat.completions.create(
            model='gpt-4-1106-preview',
            messages=[
                {
                    "role": 'assistant',
                    'content': prompt,
                },
                {
                    'role': 'user',
                    'content': text,
                },
            ],
        )

        return response.choices[0].message.content
