"""Handlers for the first user's message"""


from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp, db


@dp.message_handler(Command("runtalkie"))
async def library_command(message: Message):
    user = db.select_user(id=message.from_user.id)
    if user[11] == 0:
        db.update_is_bot_paused(1, user[0])
        await message.answer("Бот поставлен на паузу. Ты не будешь получать новые пары для тренировок\n\n"
                             "Чтобы включить бота снова напиши /runtalkie",
                         disable_notification=True)
    else:
        db.update_is_bot_paused(0, user[0])
        await message.answer("Бот снят с паузы. В 19:30 ты получишь новую пару.",
                             disable_notification=True)
