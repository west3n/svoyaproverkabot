from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def registration() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Начать регистрацию', callback_data='registration')]
    ])
    return kb
