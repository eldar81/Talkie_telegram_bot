"""This file store all keyboards"""


import random
from aiogram.utils import callback_data
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, callback_query
from config import admin_ids
from loader import dp

# Start bot
letsgo_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Поехали 🚀", callback_data="step1")
        ]
    ]
)

# Confirm correct questionnaire
bio_is_correct = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Все верно 👍", callback_data="bio_is_ok"),
            InlineKeyboardButton(text="Заполнить заново", callback_data='rewrite_anketa')
        ]
    ]
)

# Set gender
bio_gender = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[
                                      [InlineKeyboardButton(text="Мужской 🙋‍♂️", callback_data="male")],
                                      [InlineKeyboardButton(text="Женский 🙋‍♀️", callback_data="female")]
                                  ]
                                  )

# Choose companion gender
gender_of_companion = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мужского", callback_data="gender_of_companion_male")],
        [InlineKeyboardButton(text="Женского", callback_data="gender_of_companion_female")],
        [InlineKeyboardButton(text="Не важно", callback_data="gender_of_companion_both")]
    ]
)

# Profile menu
profile_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Изменить профиль ✍️", callback_data="change_my_profile")],
        [InlineKeyboardButton(text="Все верно 👍", callback_data="menu")]
    ]
)

# Profile menu changes
change_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="change_profile_name")],
        [InlineKeyboardButton(text="Пол", callback_data="change_profile_gender")],
        [InlineKeyboardButton(text="Возраст", callback_data="change_profile_age")],
        [InlineKeyboardButton(text="Интересы", callback_data="change_profile_hobby")],
        [InlineKeyboardButton(text="Пожелания к собеседнику", callback_data="change_profile_compreq")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_profile")]
    ]
)

# Profile submenu
profile_submenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="change_my_profile")],
        [InlineKeyboardButton(text="В главное меню", callback_data="menu")]
    ]
)

# Help menu
help_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Бот работает странно/не работает 🤖", callback_data="bot_bug")],
        [InlineKeyboardButton(text="Не могу с чем-то разобраться 🧐", callback_data="need_help")],
        [InlineKeyboardButton(text="Пожаловаться на пользователя 🚔", callback_data="need_help")],
        [InlineKeyboardButton(text="Другое", callback_data="need_help")],
    ]
)

# Choose task 1
choose_task1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Легкие", callback_data="easy_tasks")],
        [InlineKeyboardButton(text="❌ Средние", callback_data="medium_tasks_deny")],
        [InlineKeyboardButton(text="❌ Сложные", callback_data="hard_tasks_deny")]
    ]
)

# Choose task 2
choose_task2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Легкие", callback_data="easy_tasks")],
        [InlineKeyboardButton(text="✅ Средние", callback_data="medium_tasks")],
        [InlineKeyboardButton(text="❌ Сложные", callback_data="hard_tasks_deny")]
    ]
)

# Choose task 3
choose_task3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Легкие", callback_data="easy_tasks")],
        [InlineKeyboardButton(text="✅ Средние", callback_data="medium_tasks")],
        [InlineKeyboardButton(text="✅ Сложные", callback_data="hard_tasks")]
    ]
)

# Send easy task
send_easy_task = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Получить задание", callback_data="get_easy_task")]
    ]
)


# Send medium task
send_medium_task = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Получить задание", callback_data="get_medium_task")]
    ]
)

# Send hard task
send_hard_task = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Получить задание", callback_data="get_hard_task")]
    ]
)
support_callback = CallbackData("ask_support", "messages", "user_id", "as_user")
cancel_support_callback = CallbackData("cancel_support", "user_id")

# Did you test companion
contact_check = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да, списались", callback_data="contact_was")],
        [InlineKeyboardButton(text="Пока нет", callback_data="contact_was_not")]
    ]
)

# Did the meeting agreed
agreed_meeting_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да, договорились", callback_data="meeting_agreed")],
        [InlineKeyboardButton(text="Уже провели", callback_data="meeting_done")]
    ]
)

# Meeting is not agreed
not_agreed_meeting_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Не пытался(-ась)", callback_data="did_not_tried_to_agree_meeting")],
        [InlineKeyboardButton(text="Мне не ответили", callback_data="did_not_recieve_answer_to_agree_meeting")]
    ]
)

good_or_bad_meeting = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Хорошо 👍", callback_data="meeting_was_good")],
        [InlineKeyboardButton(text="Плохо 👎", callback_data="meeting_was_bad")]
    ]
)

do_participate_next_time = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да!", callback_data="participate_next_time")],
        [InlineKeyboardButton(text="Пока нет", callback_data="not_participate_next_time")]
    ]
)

do_another_meeting = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да!", callback_data="participate_next_time")],
        [InlineKeyboardButton(text="Пока нет", callback_data="not_participate_next_time")]
    ]
)

why_did_not_try = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Страшно/Некомфотно", callback_data="fear")],
        [InlineKeyboardButton(text="Нет потребности в боте", callback_data="do_not_need_bot")],
        [InlineKeyboardButton(text="Не хочу писать именно этому напарнику", callback_data="do_not_like_partner")],
        [InlineKeyboardButton(text="Другое", callback_data="another_reason")]
    ]
)

do_change_partner = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да, давайте поменяем", callback_data="change_partner")],
        [InlineKeyboardButton(text="Спасибо, не надо", callback_data="do_not_change_partner")]
    ]
)

another_reason_details = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Я все таки напишу своему напарнику", callback_data="do_not_change_partner")],
        [InlineKeyboardButton(text="Поменяйте мне напарника", callback_data="change_partner")],
        [InlineKeyboardButton(text="Приостановить бота", callback_data="not_participate_next_time")]
    ]
)


# Support service functions
async def check_support_available(support_id):
    state = dp.current_state(chat=support_id, user=support_id)
    state_str = str(
        await state.get_state()
    )
    if state_str == "in_support":
        return
    else:
        return support_id


async def get_support_manager():
    random.shuffle(admin_ids)
    for support_id in admin_ids:
        # Проверим если оператор в данное время не занят
        support_id = await check_support_available(support_id)

        # Если такого нашли, что выводим
        if support_id:
            return support_id
    else:
        return


async def support_keyboard(messages, user_id=None):
    if user_id:
        # If the second ID is specified, then this button is for the operator

        contact_id = int(user_id)
        as_user = "no"
        text = "Ответить"

    else:
        # If the second ID is not specified, then this button is for the user and you need to select an operator for him

        contact_id = await get_support_manager()
        as_user = "yes"
        if messages == "many" and contact_id is None:
            # Если не нашли свободного оператора - выходим и говорим, что его нет
            return False
        elif messages == "one" and contact_id is None:
            contact_id = random.choice(admin_ids)

        if messages == "one":
            text = "Рассказать о проблеме"
        else:
            text = "Написать оператору"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=support_callback.new(
                messages=messages,
                user_id=contact_id,
                as_user=as_user
            )
        )
    )

    if messages == "many":
        # Add a button to end the session if you change your mind about calling support
        keyboard.add(
            InlineKeyboardButton(
                text="Завершить сеанс",
                callback_data=cancel_support_callback.new(
                    user_id=contact_id
                )
            )
        )
    return keyboard


def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Завершить сеанс",
                    callback_data=cancel_support_callback.new(
                        user_id=user_id
                    )
                )
            ]
        ]
    )
