from aiogram.dispatcher.filters.state import State, StatesGroup


class Text(StatesGroup):
    next_sentence = State()
