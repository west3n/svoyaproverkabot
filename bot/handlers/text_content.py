import asyncio
import requests
import io

from aiogram import Dispatcher, types
from bot.json import parse
from bot.database.mysql import mysql
from bot.database.sqlite import sqlite


async def check_result(msg: types.Message):
    user_id = msg.from_user.id
    user = await sqlite.user_status(user_id)
    if not user:
        await msg.answer("Чтобы пользоваться ботом, вы должны выполнить вход - /login")
    else:
        test = msg.text
        if test.isdigit() and len(test) <= 12:
            try:
                await msg.answer(text='Бот начал сбор данных, это может занять '
                                      'от 20 секунд до 3х минут, пожалуйста, ожидайте.')
                await asyncio.sleep(7)
                await msg.answer(text="Вместе с ответом на запрос вам будет доступен PDF-файл, "
                                      "в котором будет находиться вся подробная информация.")
                inn = msg.text
                info = parse.json_parse(inn)
                if info[9]:
                    json_data = info[15]
                else:
                    json_data = info[6]
                user_id = msg.from_user.id
                u_id = await sqlite.get_id(user_id)
                text = parse.check_text(info)
                if json_data != {'message': 'Компания / ИП не найдены в ЕГРЮЛ / ЕГРИП (2)'}:
                    await mysql.update_log(user_id=u_id, data=inn, json_data=json_data)
                await msg.answer(text=text)
                await create_pdf(msg, inn)
            except:
                await msg.answer(text='По введенным данным нет информации, попробуйте ввести другие')
        else:
            await msg.answer(text='Неверный формат сообщения. Введите ИНН или ОГРН, '
                                  'используя только цифры (12 цифр максимум).')


async def create_pdf(msg: types.Message, inn: str):
    await asyncio.sleep(1)
    await msg.answer("Бот подготавливает полный отчет, пожалуйста, ожидайте.")
    url = f"https://svoya-proverka.ru/v2/export-pdf.php?ogrn={inn}&" \
          f"blocks=[%221%22,%222%22,%224%22,%225%22,%226%22,%229%22]"
    response = requests.get(url)
    with open("example.pdf", "wb") as f:
        file = f.write(response.content)
    with open("example.pdf", "rb") as f:
        file_bytes = io.BytesIO(f.read())
        input_file = types.InputFile(file_bytes, f"Полный отчет_{inn}.pdf")
    await msg.bot.send_document(msg.from_user.id, document=input_file)


def register(dp: Dispatcher):
    dp.register_message_handler(check_result, content_types="text")
    dp.register_callback_query_handler(create_pdf, text='get_pdf_file_txt')
