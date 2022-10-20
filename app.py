from aiogram import executor

from bot_commands import set_default_commands
from handlers.handlers_action import schedule_jobs
from loader import db, bot, dp, storage, scheduler
import handlers, middlewares

async def on_startup(dp):
    try:
        db.create_table_users()
    except Exception as e:
        print(e)
    try:
        db.create_table_match_gen()
        print("Match_gen table is created")
    except Exception as e:
        print(e)

    try:
        db.create_table_final_matches()
        print("Matches table is created")
    except Exception as e:
        print(e)
    schedule_jobs(17, 56)
    await set_default_commands(dp)


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
