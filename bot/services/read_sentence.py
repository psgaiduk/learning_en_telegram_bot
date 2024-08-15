from os import path
from random import choices, randint
from typing import Union

from aiogram.types import (
    CallbackQuery,
    Message,
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.dispatcher.storage import FSMContext

from bot import bot
from choices import EnglishLevels, State
from dto import TelegramUserDTOModel
from functions import get_combinations, delete_message, save_word_history, update_data_by_api


class ReadSentenceService:
    """Service for reading sentence."""

    _telegram_user: TelegramUserDTOModel
    _sentence_text: str
    _sentence_translation: str
    _message_text: str

    def __init__(self, message: Union[CallbackQuery, Message], state: FSMContext) -> None:
        """Init."""
        self._message = message
        self._state = state

    async def do(self) -> None:

        if isinstance(self._message, CallbackQuery) and "know_word_" in self._message.data:
            await delete_message(message=self._message)
            await save_word_history(callback_query=self._message)

        await self._get_telegram_user()
        await self._get_sentence()
        await self._create_keyboard()
        await self._create_file_path()
        await self._create_message_text()
        await self._send_separator()
        await self._send_message_or_tenses()

        self._telegram_user.new_sentence.text = ""
        await self._state.set_data(data={"user": self._telegram_user})

    async def _get_telegram_user(self) -> None:
        data = await self._state.get_data()
        self._telegram_user = data["user"]

    async def _get_sentence(self) -> None:
        self._sentence_text = self._telegram_user.new_sentence.text
        self._sentence_translation = self._telegram_user.new_sentence.translation.get("ru")

    async def _create_keyboard(self) -> None:
        self._keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        self._keyboard.add(KeyboardButton(text="Read"))

    async def _create_file_path(self) -> None:
        file_name = f"{self._telegram_user.new_sentence.book_id} - {self._telegram_user.new_sentence.order - 1}"
        self._file_path = f"static/audio/{file_name}.mp3"

    async def _create_message_text(self) -> None:
        if randint(1, 3) == 1 and path.isfile(self._file_path):
            await self._send_audio_message()
        else:
            self._message_text = f"{self._sentence_text}"

    async def _send_message_or_tenses(self) -> None:
        if randint(1, 5) == 1:
            await self._send_tenses()
        else:
            await self._send_message()

    async def _send_audio_message(self) -> None:
        with open(self._file_path, "rb") as audio:
            self._message_text = ""
            sentence_text = f"Text:\n\n<tg-spoiler>{self._sentence_text}</tg-spoiler>"

            await bot.send_audio(
                chat_id=self._telegram_user.telegram_id,
                audio=audio,
                caption=sentence_text,
                parse_mode=ParseMode.HTML,
                reply_markup=self._keyboard,
            )

    async def _send_tenses(self) -> None:
        is_update = await self._update_stage_user(stage=State.check_answer_time.value)
        if is_update is False:
            return

        await self._send_text_with_tenses()

    async def _send_message(self) -> None:
        is_update_sentence = await self._update_history_sentence()

        if is_update_sentence is False:
            return

        is_update_stage = await self._update_stage_user(stage=State.start_learn_words.value)
        if is_update_stage is False:
            return

        await delete_message(message=self._message)

        if self._message_text:
            await bot.send_message(
                chat_id=self._telegram_user.telegram_id,
                text=self._message_text,
                parse_mode=ParseMode.HTML,
                reply_markup=self._keyboard,
            )

        await self._send_clue()
        await self._send_translate()

    async def _send_text_with_tenses(self) -> None:
        if self._message_text:
            await bot.send_message(
                chat_id=self._telegram_user.telegram_id,
                text=self._message_text,
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardRemove(),
            )
        await self._send_clue()
        await self._send_translate()
        message_text = "К какому времени относится предложение?"
        right_answer = self._telegram_user.new_sentence.sentence_times
        count_times_in_sentence = right_answer.count(",") + 1
        all_english_times = get_combinations(count_times_in_sentence)
        all_answers = [right_answer]
        other_answers = choices(all_english_times, k=3)
        all_answers.extend(other_answers)

        sorted(all_answers, key=lambda x: randint(1, 100))
        keyboard = InlineKeyboardMarkup()
        for answer in all_answers:
            callback_data = "wrong_answer_time" if answer != right_answer else "right_answer_time"
            keyboard.add(InlineKeyboardButton(text=answer, callback_data=callback_data))

        await bot.send_message(
            chat_id=self._telegram_user.telegram_id,
            text=message_text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )

    async def _update_stage_user(self, stage: str) -> bool:
        params_for_update_user = {
            "telegram_id": self._message.from_user.id,
            "stage": stage,
        }

        return await update_data_by_api(
            telegram_id=self._message.from_user.id,
            params_for_update=params_for_update_user,
            url_for_update=f"telegram_user/{self._message.from_user.id}",
        )

    async def _update_history_sentence(self) -> bool:
        data_for_update_history_sentence = {
            "id": self._telegram_user.new_sentence.history_sentence_id,
            "is_read": True,
        }

        return await update_data_by_api(
            telegram_id=self._telegram_user.telegram_id,
            params_for_update=data_for_update_history_sentence,
            url_for_update=f"history/sentences/{self._telegram_user.new_sentence.history_sentence_id}",
        )

    async def _send_clue(self) -> None:

        clue_text = self._telegram_user.new_sentence.text_with_new_words
        if self._telegram_user.level_en.order < EnglishLevels.C1.level_order:
            clue_text = self._telegram_user.new_sentence.text_with_words

        clue_text = f"Подсказка:\n\n<tg-spoiler>{clue_text}</tg-spoiler>"
        await bot.send_message(
            chat_id=self._telegram_user.telegram_id,
            text=clue_text,
            parse_mode=ParseMode.HTML,
            reply_markup=self._keyboard,
        )

    async def _send_translate(self) -> None:
        translate_text = f"Перевод:\n\n<tg-spoiler>{self._sentence_translation}</tg-spoiler>"
        await bot.send_message(
            chat_id=self._telegram_user.telegram_id,
            text=translate_text,
            parse_mode=ParseMode.HTML,
            reply_markup=self._keyboard,
        )

    async def _send_separator(self) -> None:
        await bot.send_message(
            chat_id=self._telegram_user.telegram_id,
            text="=" * 30,
            parse_mode=ParseMode.HTML,
        )
