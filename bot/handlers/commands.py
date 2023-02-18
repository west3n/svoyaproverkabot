from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot.database.mysql import mysql
from bot.database.sqlite import sqlite
from bot.keyboards import inline
from bot import states as st
from bot.text import parse
import asyncio
import requests
import io


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
        user_id = msg.from_user.id
        bot_db = await sqlite.get_id(user_id)
        result = await mysql.get_user_profile(bot_db[0])
        date = result[1].strftime("%d.%m.%Y")
        await msg.answer(f"<em>Тариф:</em><b> {result[0]} </b>"
                         f"\n<em>Действует до:</em> <b>{date}</b>"
                         f"\n<em>Осталось проверок:</em> <b> {result[2] - 1}</b>",
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


async def check_result(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['inn'] = msg.text
    await msg.delete()
    await msg.answer(text='Идет сбор данных, ожидайте')
    await asyncio.sleep(2)
    await msg.answer(text="Для получения полной информации вы "
                          "можете скачать pdf-файл, который будет прикреплен к ответу")
    inn = data.get('inn')
    info = parse.json_parse(inn)
    json = info[9]
    user_id = msg.from_user.id
    u_id = await sqlite.get_id(user_id)
    await mysql.update_log(user_id=u_id, data=inn, json=json)
    await msg.answer(text=parse.check_text(info))
    await state.finish()


async def get_pdf_file(msg: types.Message):
    url = "https://svoya-proverka.ru/v2/export-pdf.php?ogrn=1027700132195&" \
          "blocks=[%221%22,%222%22,%224%22,%225%22,%226%22,%229%22]"
    response = requests.get(url)
    with open("example.pdf", "wb") as f:
        file = f.write(response.content)
    with open("example.pdf", "rb") as f:
        file_bytes = io.BytesIO(f.read())
        input_file = types.InputFile(file_bytes, "Подробный отчет.pdf")
    await msg.bot.send_document(msg.from_user.id, document=input_file)


def register(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands='start', state='*')
    dp.register_message_handler(bot_about, commands='about', state='*')
    dp.register_message_handler(user_login, commands='login', state='*')
    dp.register_message_handler(user_profile, commands='profile', state='*')
    dp.register_message_handler(check_inn, commands='check', state='*')
    dp.register_message_handler(get_pdf_file, commands='get_pdf', state="*")
    dp.register_message_handler(check_result, state=st.CheckInn.inn)

