"""Here I try to use Finite State Machine. It's funny"""

from aiogram.dispatcher.filters.state import StatesGroup, State


class Ankena(StatesGroup):
    Name = State()
    Age = State()
    Gender = State()
    Hobby = State()
    Comp_req = State()
