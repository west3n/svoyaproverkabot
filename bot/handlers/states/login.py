import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot import states as st
from bot.database.mysql import mysql as db
from bot.database.sqlite import sqlite
from bot.keyboards import inline
from bot.keyboards import reply


async def start_login(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    user = await sqlite.user_status(user_id)
    if not user:
        await call.message.answer(text='Введи свой логин:',
                                  reply_markup=reply.cmd_cancel())
        await st.Login.login.set()
    else:
        await call.message.answer('Вы уже вошли в аккаунт!')


async def save_login(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = msg.text
    await msg.answer(text='Введи свой пароль:',
                     reply_markup=reply.remove)
    await st.Login.next()


async def finish(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await msg.delete()
        data['password'] = msg.text
    user_exists = await db.verify_hash(data)
    if user_exists[0] is True:
        user_id = msg.from_user.id
        u_id = user_exists[1]
        display_name = user_exists[2]
        await state.finish()
        try:
            await sqlite.add_user(u_id, user_id, data, display_name)
            await asyncio.sleep(3)
            test = await profile(user_id)
            await msg.answer(f"\n<b>Ваш профиль:</b>"
                             f'\n✅<em>Добро пожаловать, <b>{test[0]}!</b></em>'
                             f"\n🌐<em>Ваш тариф:</em><b> {test[1]} </b>"
                             f"\n📅<em>Действует до:</em> <b>{test[2]}</b>"
                             f"\n📝<em>Осталось проверок:</em> <b>{test[3]}</b>\n\n",
                             reply_markup=inline.logout())
            await msg.answer(f"📑 Чтобы проверить организацию введите ИНН или ОГРН организации")
        except:
            await msg.answer(text='Вход по данному логину уже выполнен.\nИспользуйте другой - /start.')
    elif user_exists[0] is False:
        await state.finish()
        await msg.answer(text=f'Неправильный логин или пароль.\n'
                              f'Попробовать заново - /start\n\n'
                              f'Забыли пароль? <a href= "https://svoya-proverka.ru/password-reset/">'
                              f'Сброс пароля</a>')


async def cmd_cancel(msg: types.Message, state: FSMContext):
    await msg.answer(text='Вы отменили действие!',
                     reply_markup=reply.remove)
    await state.finish()


async def profile(user_id):
    bot_db = await sqlite.get_id(user_id)
    display_name = await sqlite.get_display_name(user_id)
    result = await db.get_user_profile(bot_db[0])
    tarif = result[0]
    date = result[1].strftime("%d.%m.%Y")
    col = result[2]
    count = await db.count_scoring(bot_db[0])
    test = col - count
    return display_name, tarif, date, test


def register(dp: Dispatcher):
    dp.register_callback_query_handler(start_login, text='login')
    dp.register_message_handler(cmd_cancel, text='Отмена', state="*")
    dp.register_message_handler(save_login, content_types=['text'], state=st.Login.login)
    dp.register_message_handler(finish, content_types=['text'], state=st.Login.password)
