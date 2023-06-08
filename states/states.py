from aiogram.dispatcher.filters.state import State, StatesGroup

class NumberState(StatesGroup):
    phone = State()