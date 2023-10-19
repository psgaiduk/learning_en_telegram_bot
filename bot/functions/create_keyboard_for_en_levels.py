from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def create_keyboard_for_en_levels(hero_level: int) -> InlineKeyboardMarkup:
    """
    Create keyboard for en levels.

    :param hero_level: user's hero level.
    :return: keyboard with buttons lelels
    """
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text='A1 - Beginner', callback_data='level_en_1'))
    inline_keyboard.add(InlineKeyboardButton(text='A2 - Elementary', callback_data='level_en_2'))

    level_buttons = [
        {'hero_level': 10, 'text': 'B1 - Pre-intermediate', 'callback_data': 'level_en_3'},
        {'hero_level': 25, 'text': 'B2 - Intermediate', 'callback_data': 'level_en_4'},
        {'hero_level': 50, 'text': 'C1 - Upper-intermediate', 'callback_data': 'level_en_5'},
        {'hero_level': 80, 'text': 'C2 - Advanced', 'callback_data': 'level_en_6'},
    ]

    for button in level_buttons:
        if hero_level > button['hero_level']:
            inline_keyboard.add(InlineKeyboardButton(text=button['text'], callback_data=button['callback_data']))

    return inline_keyboard
