from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def login() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Зайти в свой аккаунт', callback_data='login')]
    ])
    return kb


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


def get_pdf_file() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Получить полный отчет в PDF-формате', callback_data='get_pdf_file')]
    ])
    return kb
