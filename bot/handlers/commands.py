from aiogram import Dispatcher, types
from bot.keyboards import inline


async def bot_start(msg: types.Message):
    user_name = msg.from_user.first_name
    await msg.delete()
    await msg.answer(text=f'Привет, {user_name}!', reply_markup=inline.registration())


async def bot_help(msg: types.Message):
    await msg.delete()
    await msg.answer("Здесь текст с информацией о работе бота")


async def bot_about(msg: types.Message):
    await msg.delete()
    await msg.answer("Здесь текст с информацией о компании")


def register(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands='start', state='*')
    dp.register_message_handler(bot_help, commands='help', state='*')
    dp.register_message_handler(bot_about, commands='about', state='*')
