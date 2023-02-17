from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot import states as st
from bot.database.mysql import add_users as db
from bot.database.sqlite.sqlite import add_user as sqlite_db

from passlib.hash import phpass


async def start_login(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(text='Введи свой логин:')
    await st.Login.login.set()


async def save_login(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = msg.text
    await msg.answer(text='Введи свой пароль:')
    await st.Login.next()


async def finish(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await msg.delete()
        data['password'] = msg.text
    user_exists = await db.check_user_db(data)
    if user_exists:
        user_id = msg.from_user.id
        await state.finish()
        try:
            await sqlite_db(user_id, data)
            await msg.answer(text='Вход в аккаунт выполнен.\nПосмотреть профиль - /profile'
                                  '\nПроверить компанию по ОГРН - /check')
        except:
            await msg.answer(text='Вход по данному логину уже выполнен.\nИспользуйте другой - /login.')
    else:
        await state.finish()
        await msg.answer(text='Неправильный логин или пароль.\nПопробовать заново - /login')


def register(dp: Dispatcher):
    dp.register_callback_query_handler(start_login, text='login')
    dp.register_message_handler(save_login, content_types=['text'], state=st.Login.login)
    dp.register_message_handler(finish, content_types=['text'], state=st.Login.password)
