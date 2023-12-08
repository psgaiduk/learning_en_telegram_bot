from openai import OpenAI

from settings import settings


class AISDK:
    """Класс для работы с OpenAI API."""

    def __init__(self):
        self._client = OpenAI(api_key=settings.ai_token)

    async def get_words(self, sentence: str, english_level: str) -> list[str]:
        """
        Получить слова из предложения.

        :param sentence: предложение.
        :param english_level: уровень английского.
        :return: список слов.
        """

        response = self._client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    "role": 'assistant',
                    'content': f'Как учитель английского языка с 30-летним опытом, проанализируйте следующее предложение ученика и выделите все '
                               f'идиомы, фразовые  глаголы и сложные слова, которые может не знать ученик уровня {english_level}, указав их '
                               f'через запятую. Перевод давать не надо, просто напиши их через запятую',
                },
                {
                    'role': 'user',
                    'content': sentence,
                },
            ],
        )

        return response.choices[0].message.content.split(',')
