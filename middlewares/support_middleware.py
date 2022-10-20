"""Midleware written to work with online support"""


from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import dp


# Create a middleware that will completely process messages
# for the user and operators who are online.
# Messages will not even be sent to handlers from here
class SupportMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Get the state of the current user,since state: FSMContext will not get here
        state = dp.current_state(chat=message.from_user.id, user=message.from_user.id)

        # Get the string value of the state and compare it
        state_str = str(await state.get_state())
        if state_str == "in_support":

            # Take the ID of the second user and send him a message
            data = await state.get_data()
            second_id = data.get("second_id")
            await message.copy_to(second_id)

            # Do not skip further processing in handlers
            raise CancelHandler()
