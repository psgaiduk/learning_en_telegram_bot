from re import match

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from bot import dispatcher
from choices import State
from services import WaitNameService


@dispatcher.message_handler(lambda message: message.text and match(r'^[\w]+$', message.text), state=State.wait_name.value)
async def handle_wait_name(message: Message, state: FSMContext):
    """Handle wait name."""
    await WaitNameService(message=message, state=state).do()


@dispatcher.message_handler(lambda message: message.text and not match(r'^[\w]+$', message.text), state=State.wait_name.value)
async def handle_wait_name_incorrect_work(message: Message):
    """Handle wait name."""
    await message.answer('Имя надо вводить одним слово, без использования специальных символов. Попробуйте еще раз.')
