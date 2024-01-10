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

        prompt = """Вы преподаватель английского языка с 30-летним опытом.
Ученик сейчас на уровне знаний A1 - Elementary 
и он отправит тебе текст.
Разбейте это на предложения
Вы должны перевести каждую часть на русский язык.

Проанализируй предложения и в каждом выдели слова которые ученик может не знать на этом уровне, не надо выделять все слова:
3. идиомы и стандартные литературные обороты, такие как (once upon a time, In times of old и другие)
2. фразовые глаголы (Пример: such as, bring up, put up и другие).
1. сложные слова (Пример: word, time, tulip и др.), отбрасывай артикли, притяжательные местоимения, вспомогательные глаголы, предлоги, прилагательные. 
Перевод для слов давать не надо, просто раздели их между собой через ; и для каждого типа проставь номер 1, 2 или 3 в зависимости от типа слова. 

Дополнительно выполнить анализ времени в предложении напиши к какому времени оно относится.

Далее дай пояснение, почему именно это время тут должно использоваться.

каждую часть отделяй от другой использую ---.

Итак твой ответ должен содержать 5 блоков по каждому предложению, каждый блок должен быть обязательно:
Предожение на английском --- Перевод этого предложения --- Сложные слова с переводом --- Время предложения --- Объяснение почему именно это время
Новая строка только для новного предложания.

Пример как это должно работать:
Ученик присылает тебе текст:
At first, it was small and weak, but she watered it and told it stories, and over the years, it got bigger and bigger. At first, it was small and weak, but she watered it and told it stories, and over the years, it got bigger and bigger.

Твой ответ:
At first, it was small and weak, but she watered it and told it stories, and over the years, it got bigger and bigger.  --- Сначала он был маленьким и слабым, но она поливала его и рассказывала ему истории, и с годами он становился все больше  и больше. --- at first - 3; watered - 1;  told - 1;  stories - 1  -- Past Simple --- Past Simple используется здесь, потому что предложение описывает завершенное действие или состояние в прошлом. Признаки: использование формы "was" для глагола "to be" для описания прошлого.

On Fridays, Sarah and her friends go out on the town, painting it red as they explore new restaurants. --- По пятницам Сара и ее друзья выходят в город, оживляя его своим присутствием и исследуя новые рестораны. --- on the town- 3; painting it red - 3; go out - 2; explore - 1; restaurants - 1; --- Present Simple --- В предложении описывается регулярное событие, которое происходит каждую пятницу (On Fridays). Present Simple используется для выражения повторяющихся действий в настоящем времени.

"""

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


if __name__ == '__main__':
    print(AISDK().translate_and_analyse('There was once upon a time an old goat who had seven little kids, and loved them with all the love of a mother for her children. One day she wanted to go into the forest and fetch some food.'))
