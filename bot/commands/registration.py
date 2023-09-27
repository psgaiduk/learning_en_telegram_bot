from aiogram import types

from bot import dispatcher
from services import RegistrationService


@dispatcher.message_handler(state='REGISTRATION', commands=['start'])
async def handle_registration(message: types.Message):
    """Handle registration."""
    await RegistrationService(message=message).do()
