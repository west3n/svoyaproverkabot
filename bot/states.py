from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    login = State()
    password = State()
