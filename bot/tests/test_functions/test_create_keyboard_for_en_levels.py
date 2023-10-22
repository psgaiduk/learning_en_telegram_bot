from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytest import mark

from functions import create_keyboard_for_en_levels


class TestCreateKeyboardForEnLevelsFunction:
    """Tests for create_keyboard_for_en_levels function."""

    @mark.parametrize('hero_level_order, buttons_count', [
        (0, 2), (10, 2), (11, 3), (25, 3), (26, 4), (30, 4), (50, 4), (51, 5), (60, 5), (80, 5), (81, 6), (90, 6),
    ])
    @mark.asyncio
    async def test_create_keyboard(self, hero_level_order, buttons_count):

        expected_buttons = [
            [InlineKeyboardButton(text='A1 - Beginner', callback_data='level_en_1')],
            [InlineKeyboardButton(text='A2 - Elementary', callback_data='level_en_2')],
            [InlineKeyboardButton(text='B1 - Pre-intermediate', callback_data='level_en_3')],
            [InlineKeyboardButton(text='B2 - Intermediate', callback_data='level_en_4')],
            [InlineKeyboardButton(text='C1 - Upper-intermediate', callback_data='level_en_5')],
            [InlineKeyboardButton(text='C2 - Advanced', callback_data='level_en_6')],
        ]

        expected_inline_kd = InlineKeyboardMarkup()
        for button in expected_buttons[:buttons_count]:
            expected_inline_kd.add(*button)

        inline_kd = await create_keyboard_for_en_levels(hero_level=hero_level_order)

        assert inline_kd == expected_inline_kd
