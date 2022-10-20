"""Handlers for after match messages"""

import asyncio
from datetime import date

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import contact_check, agreed_meeting_kb, not_agreed_meeting_kb, \
    good_or_bad_meeting, do_participate_next_time, why_did_not_try, do_another_meeting, do_change_partner, \
    another_reason_details
from loader import dp, db


# 1.Списались с напарником?
async def was_contact_asking(dp: Dispatcher):
    matches = db.select_all_matches()
    todaydate = int(str(date.today()).replace("-", ""))
    print(todaydate)
    print(type(todaydate))
    for i in matches:
        if i[9] is None and i[10] is None and i[3] != todaydate:  # Если поля was_contact1 и was_contact2 пустые и date != сегодня
            try:
                id1 = i[1]
                id2 = i[2]
                await dp.bot.send_message(id1, "Вы списались с вашим напарником?", reply_markup=contact_check)
                db.update_was_contact1(2, i[0])  # ставим полю was_contact1 значение 2, что означает "вопрос отправлен"
                await asyncio.sleep(.05)
                await dp.bot.send_message(id2, "Вы списались с вашим напарником?", reply_markup=contact_check)
                db.update_was_contact2(2, i[0])  # ставим полю was_contact2 значение 2, что означает "вопрос отправлен"
                await asyncio.sleep(.05)
            except Exception as e:
                print(f"Ошибка. Match {i[0]}: {e}")


# 1.1. Да списались
@dp.callback_query_handler(text='contact_was')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_was_contact1(1, match[0][0])  # ставим полю was_contact1 значение 1, что означает "да"
        db.update_meeting_agreed_1(2, match[0][0])
        await call.message.answer("Вы договорились о встрече?", reply_markup=agreed_meeting_kb,
                                  disable_notification=True)
        await call.message.edit_reply_markup()
    else:
        await call.answer(cache_time=5)
        db.update_was_contact2(1, match[0][0])  # ставим полю was_contact2 значение 1, что означает "да"
        db.update_meeting_agreed_2(2, match[0][0])
        await call.message.answer("Вы договорились о встрече?", reply_markup=agreed_meeting_kb,
                                  disable_notification=True)
        await call.message.edit_reply_markup()


# 1.2. Нет, не списались
@dp.callback_query_handler(text='contact_was_not')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_was_contact1(0, match[0][0])  # ставим полю was_contact1 значение 0, что означает "нет"
        await call.message.answer("Почему?", reply_markup=not_agreed_meeting_kb,
                                  disable_notification=True)
        await call.message.edit_reply_markup()
    else:
        await call.answer(cache_time=5)
        db.update_was_contact2(0, match[0][0])  # ставим полю was_contact2 значение 0, что означает "нет"
        await call.message.answer("Почему?", reply_markup=not_agreed_meeting_kb,
                                  disable_notification=True)
        await call.message.edit_reply_markup()


# 1.1.1 Да, договорились о встрече
@dp.callback_query_handler(text='meeting_agreed')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_meeting_agreed_1(1, match[0][0])
        db.sql_update_function("Matches", "write_again_1", 1, "id1_id2_date", match[0][0])
        await call.message.answer("Отлично! Напишу через пару дней узнать, как все прошло :)",
                                  disable_notification=True)
        await call.message.edit_reply_markup()
    else:
        await call.answer(cache_time=5)
        db.update_meeting_agreed_2(1, match[0][0])
        db.sql_update_function("Matches", "write_again_2", 1, "id1_id2_date", match[0][0])
        await call.message.answer("Отлично! Напишу через пару дней узнать, как все прошло :)",
                                  disable_notification=True)
        await call.message.edit_reply_markup()


# 1.1.2 Встречу уже провели
@dp.callback_query_handler(text='meeting_done')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_meeting_agreed_1(1, match[0][0])
        db.update_meeting_done_1(1, match[0][0])
        await call.message.answer("Как все прошло?", reply_markup=good_or_bad_meeting,
                                  disable_notification=True)
        await call.message.edit_reply_markup()
    else:
        await call.answer(cache_time=5)
        db.update_meeting_agreed_2(1, match[0][0])
        db.update_meeting_done_2(1, match[0][0])
        await call.message.answer("Как все прошло?", reply_markup=good_or_bad_meeting,
                                  disable_notification=True)
        await call.message.edit_reply_markup()


# 1.1.2.1 Все прошло хорошо
@dp.callback_query_handler(text='meeting_was_good')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_rate_meeting_1(1, match[0][0])
        await call.message.answer("Участвуешь в следующий раз?", reply_markup=do_participate_next_time,
                                  disable_notification=True)
        await call.message.edit_reply_markup()
    else:
        await call.answer(cache_time=5)
        db.update_rate_meeting_2(1, match[0][0])
        await call.message.answer("Участвуешь в следующий раз?", reply_markup=do_participate_next_time,
                                  disable_notification=True)
        await call.message.edit_reply_markup()


# 1.1.2.2 Все прошло плохо
@dp.callback_query_handler(text='meeting_was_bad')
async def agreed_meeting(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_rate_meeting_1(0, match[0][0])
        await call.message.answer("Скажи, что пошло не так?",
                                  disable_notification=True)
        await call.message.edit_reply_markup()
        await state.set_state("what_was_wrong")
    else:
        await call.answer(cache_time=5)
        db.update_rate_meeting_2(0, match[0][0])
        await call.message.answer("Скажи, что пошло не так?",
                                  disable_notification=True)
        await call.message.edit_reply_markup()
        await state.set_state("what_was_wrong")


# 1.1.2.1.1 Да, участвую в следующий раз
@dp.callback_query_handler(text='participate_next_time')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    print(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_want_more_1(1, match[0][0])
        db.update_in_work_0((str(user_id),))
        await call.message.answer("Отлично! Жди нового напарника завтра в 19:30",
                                  disable_notification=True)
        await call.message.edit_reply_markup()
    else:
        await call.answer(cache_time=5)
        db.update_want_more_2(1, match[0][0])
        db.update_in_work_0((str(user_id),))
        await call.message.answer("Отлично! Жди нового напарника завтра в 19:30",
                                  disable_notification=True)
        await call.message.edit_reply_markup()


# 1.1.2.1.2 Нет, не участвую в следующий раз
@dp.callback_query_handler(text='not_participate_next_time')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_want_more_1(0, match[0][0])
        db.update_is_bot_paused(1, user_id)
        db.update_in_work_0((str(user_id),))
        await call.message.answer(
            "Хорошо, мы поставили бота на паузу. Если захочешь снова поучаствовать напиши /runtalkie",
            disable_notification=True)
        await call.message.edit_reply_markup()
    else:
        await call.answer(cache_time=5)
        db.update_want_more_2(0, match[0][0])
        db.update_is_bot_paused(1, user_id)
        await call.message.answer(
            "Хорошо, мы поставили бота на паузу. Если захочешь снова поучаствовать напиши /runtalkie",
            disable_notification=True)
        await call.message.edit_reply_markup()


# 1.1.2.2.1 Рассказывает, что было плохо
@dp.message_handler(state="what_was_wrong")
async def agreed_meeting(message: Message, state: FSMContext):
    user_id = message.from_user.id
    match = db.select_match_for_task(user_id)
    answer = message.text
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        db.update_comment_meeting_1(answer, match[0][0])
        await message.answer(f"Спасибо, что поделился(-ась)"
                             f"Мы учтем твой комментарий, чтобы сделать сервис лучше:\n\n"
                             f"<i>{answer}</i>\n\n"
                             f"Ты готов(-а) попробовать пройти тренировку еще раз?",
                             reply_markup=do_another_meeting,
                             disable_notification=True)
        await state.finish()
    else:
        db.update_comment_meeting_2(answer, match[0][0])
        await message.answer(f"Спасибо, что поделился(-ась)"
                             f"Мы учтем твой комментарий, чтобы сделать сервис лучше:\n\n"
                             f"<i>{answer}</i>\n\n"
                             f"Ты готов(-а) попробовать пройти тренировку еще раз?",
                             reply_markup=do_another_meeting,
                             disable_notification=True)
        await state.finish()


# 1.2.1 Не пытался связвться
@dp.callback_query_handler(text='did_not_tried_to_agree_meeting')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_why_was_not_contact_1(1, match[0][0])
        await call.message.answer("Почему?", reply_markup=why_did_not_try,
                                  disable_notification=True)
        await call.message.edit_reply_markup()
    else:
        await call.answer(cache_time=5)
        db.update_why_was_not_contact_2(1, match[0][0])
        await call.message.answer("Почему?", reply_markup=why_did_not_try,
                                  disable_notification=True)
        await call.message.edit_reply_markup()


# 1.2.1.1 Не хочу писать этому напарнику
@dp.callback_query_handler(text='do_not_like_partner')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_why_did_not_write_1(1, match[0][0])
        await call.message.answer("Поменять для тебя напарника?", reply_markup=do_change_partner,
                                  disable_notification=True)
        await call.message.edit_reply_markup()
    else:
        await call.answer(cache_time=5)
        db.update_why_did_not_write_2(1, match[0][0])
        await call.message.answer("Поменять для тебя напарника?", reply_markup=do_change_partner,
                                  disable_notification=True)
        await call.message.edit_reply_markup()


# 1.2.1.2 Другая причина
@dp.callback_query_handler(text='another_reason')
async def agreed_meeting(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        await call.answer(cache_time=5)
        db.update_why_did_not_write_1(2, match[0][0])
        await call.message.answer("Скажи, что пошло не так?",
                                  disable_notification=True)
        await call.message.edit_reply_markup()
        await state.set_state("why_did_not_write")
    else:
        await call.answer(cache_time=5)
        db.update_why_did_not_write_2(2, match[0][0])
        await call.message.answer("Скажи, что пошло не так?",
                                  disable_notification=True)
        await call.message.edit_reply_markup()
        await state.set_state("why_did_not_write")


# 1.2.1.2.1 Рассказывает, что было плохо
@dp.message_handler(state="why_did_not_write")
async def agreed_meeting(message: Message, state: FSMContext):
    user_id = message.from_user.id
    match = db.select_match_for_task(user_id)
    answer = message.text
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        db.sql_update_function("Matches", "comment_why_did_not_write_1", answer, "id1_id2_date", match[0][0])
    else:
        db.sql_update_function("Matches", "comment_why_did_not_write_2", answer, "id1_id2_date", match[0][0])
    await message.answer(f"Спасибо, что поделился(-ась)"
                         f"Мы учтем твой комментарий, чтобы сделать сервис лучше:\n\n"
                         f"<i>{answer}</i>\n\n"
                         f"Что нам лучше сейчас сделать?",
                         reply_markup=another_reason_details,
                         disable_notification=True)
    await state.finish()


# 1.2.1.3 Говорит, что не писал, потому что стращно
@dp.callback_query_handler(text='fear')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        db.sql_update_function("Matches", "why_did_not_write_1", 3, "id1_id2_date", match[0][0])
        db.sql_update_function("Matches", "write_again_1", 1, "id1_id2_date", match[0][0])
    else:
        db.sql_update_function("Matches", "why_did_not_write_2", 3, "id1_id2_date", match[0][0])
        db.sql_update_function("Matches", "write_again_2", 1, "id1_id2_date", match[0][0])
    await call.message.answer(
        f"У нас есть база знаний (/library), которая поможет тебе преодолеть стресс. Почитай. Напишу через пару дней.",
        disable_notification=True)
    await call.message.edit_reply_markup()


# 1.2.1.4 Говорит, что не писал, потому что нет потребности в боте
@dp.callback_query_handler(text='do_not_need_bot')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        db.sql_update_function("Matches", "why_did_not_write_1", 4, "id1_id2_date", match[0][0])
    else:
        db.sql_update_function("Matches", "why_did_not_write_2", 4, "id1_id2_date", match[0][0])
    db.sql_update_function("Users", "is_bot_paused", 1, "id", user_id)  # Ставим бота на паузу
    db.sql_update_function("Users", "in_work", 0, "id", user_id)  # Убираем пользователя из работы
    await call.message.answer(
        f"Хорошо, мы поставили бота на паузу. Если захочешь снова поучаствовать напиши /runtalkie",
        disable_notification=True)
    await call.message.edit_reply_markup()


# 1.2.2 Не ответили
@dp.callback_query_handler(text='did_not_recieve_answer_to_agree_meeting')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        db.sql_update_function("Matches", "why_was_not_contact_1", 2, "id1_id2_date", match[0][0])
    else:
        db.sql_update_function("Matches", "why_was_not_contact_2", 2, "id1_id2_date", match[0][0])
    await call.message.answer(f"Поменять для тебя напарника?",
                              reply_markup=do_change_partner,
                              disable_notification=True)
    await call.message.edit_reply_markup()


# 1.2.2.1 Поменяйте мне напарника
@dp.callback_query_handler(text='change_partner')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        db.sql_update_function("Matches", "change_companion_1", 1, "id1_id2_date", match[0][0])
        partner_id = match[0][2]
    else:
        db.sql_update_function("Matches", "change_companion_2", 1, "id1_id2_date", match[0][0])
        partner_id = match[0][1]
    db.sql_update_function("Users", "in_work", 0, "id",
                           user_id)  # Меняем статус пользователя попросившего сменить напарника
    db.sql_update_function("Users", "in_work", 0, "id", partner_id)  # Меняем статус напарника
    await call.message.answer(f"Ты получишь нового напарника для тренировок в 19:30. Ожидай.",
                              disable_notification=True)
    await dp.bot.send_message(partner_id,
                              "Привет! Твой последний напарник покинул Talkie. В 19:30 мы пришлем тебе нового.")
    await call.message.edit_reply_markup()


# 1.2.2.2 Не меняйте мне напарника
@dp.callback_query_handler(text='do_not_change_partner')
async def agreed_meeting(call: CallbackQuery):
    user_id = call.from_user.id
    match = db.select_match_for_task(user_id)
    if match[0][1] == user_id:  # Если id отправителя сообщение записано в id1
        db.sql_update_function("Matches", "change_companion_1", 0, "id1_id2_date", match[0][0])
        db.sql_update_function("Matches", "write_again_1", 1, "id1_id2_date", match[0][0])
    else:
        db.sql_update_function("Matches", "change_companion_2", 0, "id1_id2_date", match[0][0])
        db.sql_update_function("Matches", "write_again_2", 1, "id1_id2_date", match[0][0])
    await call.message.answer(f"Хорошо, тогда напишем через пару дней еще раз. Постарайся связаться с напарником.",
                              disable_notification=True)
    await call.message.edit_reply_markup()
