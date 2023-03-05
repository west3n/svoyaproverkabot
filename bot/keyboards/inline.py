from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def logout() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Выйти из аккаунта', callback_data='logout_verify')]
    ])
    return kb


def confirm_logout() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton('Да', callback_data='logout'),
         InlineKeyboardButton('Нет', callback_data='cancel_logout')]
    ])
    return kb


def login() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [InlineKeyboardButton('Вход', callback_data='login'),
         InlineKeyboardButton('Регистрация', url='https://svoya-proverka.ru/register/')]
    ])

    return kb


def sup() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
         [InlineKeyboardButton('Отмена', callback_data='sup_no')]
    ])
    return kb


def sup_answer(user_name) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
         [InlineKeyboardButton('Ответить', url=f'https://t.me/{user_name}', callback_data='sup_1')]
    ])
    return kb
