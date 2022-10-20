"""Handlers for messages in /menu menu"""

from aiogram.types import CallbackQuery

from loader import dp, db


@dp.callback_query_handler(text='menu')
async def what_to_change(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer(text="Ты в главном меню\n\n"
                                   "Чтобы воспользоваться функционалом бота напиши '/' или нажми на кнопку 'Меню'",
                              disable_notification = True)
    await call.message.edit_reply_markup()