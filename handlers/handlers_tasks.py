"""Handlers for sending tasks to users"""


from random import choice
from aiogram.types import CallbackQuery

from keyboards import send_easy_task, send_medium_task, send_hard_task
from loader import dp, db
from tasks.easy_tasks import easy_tasks_list


async def send_task_part1(call, id1_id2_date):
    task_id = easy_tasks_list.index(choice(easy_tasks_list))
    task_text = easy_tasks_list[task_id][0]
    await call.message.answer(task_text)
    db.update_task(task_id, id1_id2_date)

async def send_task_part2(id1_id2_date, call):
    task_id = db.select_task_id((str(id1_id2_date),))
    task_text = easy_tasks_list[task_id[0]][1] # For some reason task_id is returned as a tuple of 1 element
    await call.message.answer(task_text)


# Refusal to give hard tast
@dp.callback_query_handler(text='hard_tasks_deny')
async def hard_tasks_deny(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer("🤖 Сложные задания открываются после 3 тренировок. Выбери уровень проще")


# Refusal to give medium task
@dp.callback_query_handler(text='medium_tasks_deny')
async def medium_tasks_deny(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer("🤖 Средние задания открываются после 1 тренировки. Выбери уровень проще")


# User choose easy task
@dp.callback_query_handler(text='easy_tasks') # ПОЛЬЗОВАТЕЛЬ ВЫБРАЛ ЛЕГКОЕ ЗАДАНИЕ
async def easy_tasks(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer("У нас есть база заданий, нажми на кнопку, и мы пришлем одно случайное\n\n"
                              "Задания парные. Это значит, что твоему напарнику придет задание дополняющее твое. "
                              "Это даст разговору русло и поможет сделать его наполенным и интересным.",
                              reply_markup=send_easy_task)
    await call.message.edit_reply_markup()


# User choose medium task
@dp.callback_query_handler(text='medium_tasks')
async def medium_tasks(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer("У нас есть база заданий, нажми на кнопку, и мы пришлем одно случайное\n\n"
                              "Задания парные. Это значит, что твоему напарнику придет задание дополняющее твое. "
                              "Это даст разговору русло и поможет сделать его наполенным и интересным.",
                              reply_markup=send_medium_task)
    await call.message.edit_reply_markup()


# User choose hard task
@dp.callback_query_handler(text='hard_tasks')
async def hard_tasks(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer("У нас есть база заданий, нажми на кнопку, и мы пришлем одно случайное\n\n"
                              "Задания парные. Это значит, что твоему напарнику придет задание дополняющее твое. "
                              "Это даст разговору русло и поможет сделать его наполенным и интересным.",
                              reply_markup=send_hard_task)
    await call.message.edit_reply_markup()


# Send easy task
@dp.callback_query_handler(text='get_easy_task')
async def get_easy_task(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # If the user id is stored in id1 in the Matches table
        if match[0][7] == 1:
            db.set_get_task1(match[0][0])  # Write get_task1 = 1
            await send_task_part2(match[0][0], call)  # Sending the second part of the task
        else:
            db.set_get_task1(match[0][0])  # Write get_task2 = 1
            # Select a random task and send the first part, set the task_id in the Matches table
            await send_task_part1(call, match[0][0])
    else:
        if match[0][6] == 1:
            print(f'Из большой формулы: {match[0][0]}')
            db.set_get_task2(match[0][0])  # Write get_task1 = 1
            await send_task_part2(match[0][0], call)  # Sending the second part of the task
        else:
            db.set_get_task2(match[0][0])  # Записывем get_task2 = 1
            # Select a random task and send the first part, set the task_id in the Matches table
            await send_task_part1(call, match[0][0])


# Send meduim task (needs to be finished)
@dp.callback_query_handler(text='get_medium_task')
async def get_medium_task(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer("Отправляю среднее задание...")
    await call.message.edit_reply_markup()


# Send hard task (needs to be finished)
@dp.callback_query_handler(text='get_hard_task')
async def get_hard_task(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer("Отправляю сложное задание...")
    await call.message.edit_reply_markup()





