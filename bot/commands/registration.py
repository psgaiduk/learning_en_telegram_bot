from aiogram import types

from bot import dispatcher
from choices import State
from services import RegistrationService


@dispatcher.message_handler(state=State.registration.value, commands=['start'])
async def handle_registration(message: types.Message) -> None:
    """Handle registration."""
    await RegistrationService(message=message).do()
