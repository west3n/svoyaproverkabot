from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
remove = ReplyKeyboardRemove()

def cmd_cancel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Отмена')]
    ], resize_keyboard=True)

    return kb

