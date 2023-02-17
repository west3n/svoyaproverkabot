from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from bot import states as st
from bot.database import create_table as db


async def start_registration(call: types.CallbackQuery):
    await call.message.answer(text='Введи свой логин:')
    await st.Registration.login.set()


async def save_login(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = msg.text
    await msg.answer(text='Введи свой пароль:')
    await st.Registration.next()


async def finish(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = msg.text
        await state.finish()
        await msg.answer(text='Регистрация завершена успешно')
        await db.create_user_db(data)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(start_registration, text='registration')
    dp.register_message_handler(save_login, content_types=['text'], state=st.Registration.login)
    dp.register_message_handler(finish, content_types=['text'], state=st.Registration.password)
