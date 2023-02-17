from aiogram import Dispatcher, types
from bot.database.sqlite import sqlite
from bot.keyboards import inline
from bot import states as st


async def bot_start(msg: types.Message):
    user_name = msg.from_user.first_name
    user_id = msg.from_user.id
    user = await sqlite.user_status(user_id)
    await msg.delete()
    if not user:
        await msg.answer(text=f'Привет, {user_name}! Зайти в свой аккаунт - /login')
    else:
        await msg.answer(text=f'Привет, {user_name}! Посмотреть свой профиль - /profile')


async def bot_about(msg: types.Message):
    await msg.delete()
    await msg.answer("<a href='https://svoya-proverka.ru/'>Своя проверка</a>"
                     " - это компания, которая умеет вот это, а ещё умеет вот это")


async def user_login(msg: types.Message):
    await msg.delete()
    user_id = msg.from_user.id
    user = await sqlite.user_status(user_id)
    if not user:
        await msg.answer("Нажмите на кнопку, чтобы выполнить вход"
                         "\n\nЕсли вы еще не зарегистрированы, "
                         "<a href='https://svoya-proverka.ru/register/'>нажмите сюда</a>",
                         reply_markup=inline.login())
    else:
        await msg.answer('Вы уже вошли в аккаунт!')


async def user_profile(msg: types.Message):
    await msg.delete()
    user_id = msg.from_user.id
    user = await sqlite.user_status(user_id)
    if not user:
        await msg.answer("Чтобы посмотреть свой профиль, вы должны выполнить вход - /login")
    else:
        await msg.answer("Тариф:"
                         "\nДействует до:"
                         "\nОсталось проверок:",
                         reply_markup=inline.logout())


async def check_inn(msg: types.Message):
    await msg.delete()
    user_id = msg.from_user.id
    user = await sqlite.user_status(user_id)
    if not user:
        await msg.answer("Чтобы пользоваться ботом, вы должны выполнить вход - /login")
    else:
        await msg.answer('Введите ИНН/ОГРН компании, которую хотите проверить:')
        await st.CheckInn.inn.set()


def register(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands='start', state='*')
    dp.register_message_handler(bot_about, commands='about', state='*')
    dp.register_message_handler(user_login, commands='login', state='*')
    dp.register_message_handler(user_profile, commands='profile', state='*')
    dp.register_message_handler(check_inn, commands='check', state='*')
