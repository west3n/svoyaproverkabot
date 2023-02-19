from aiogram.dispatcher.filters.state import State, StatesGroup


class Login(StatesGroup):
    login = State()
    password = State()


class CheckInn(StatesGroup):
    inn = State()
    ogrn = State()
