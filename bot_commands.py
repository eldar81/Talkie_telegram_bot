"""File sets up user bot menu"""


from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("profile", "Изменить профиль"),
        types.BotCommand("support", "Написать сообщение техподдержку"),
        types.BotCommand("library", "Полезные материалы")
    ])