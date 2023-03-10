from aiogram.dispatcher.filters.state import State, StatesGroup


class TextStates(StatesGroup):
    next_sentence = State()
