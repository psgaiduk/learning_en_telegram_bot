from re import match

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from bot import bot, dispatcher
from choices import State
from services import WaitNameService


@dispatcher.message_handler(lambda message: message.text and match(r'^[\w]+$', message.text), state=State.wait_name.value)
async def handle_wait_name(message: Message, state: FSMContext):
    """Handle wait name."""
    await WaitNameService(message=message, state=state).do()


@dispatcher.message_handler(state=State.wait_name.value)
async def handle_wait_name_incorrect_work(message: Message):
    """Handle wait name with wrong text."""
    await bot.send_message(message.from_user.id, 'Имя надо вводить одним слово, без использования специальных символов. Попробуйте еще раз.')


@dispatcher.callback_query_handler(state=State.wait_name.value)
async def handle_wait_name_incorrect_work_buttons(callback_query: CallbackQuery):
    """Handle wait name with push button."""
    await bot.send_message(callback_query.from_user.id, 'Имя надо отправить как сообщение. Попробуйте еще раз.')
