import asyncio
import requests
import io

from aiogram import Dispatcher, types
from bot.json import parse
from bot.database.mysql import mysql
from bot.database.sqlite import sqlite


async def check_result(msg: types.Message):
    if msg.chat.type == 'private':
        user_id = msg.from_user.id
        user = await sqlite.user_status(user_id)
        if not user:
            await msg.answer("Чтобы пользоваться ботом, вы должны выполнить вход - /start")
        else:
            try:
                bot_db = await sqlite.get_id(user_id)
                result = await mysql.get_user_profile(bot_db[0])
                count = await mysql.count_scoring(bot_db[0])
                x = result[2] - count
                if x > 0:
                    test = msg.text
                    if test.isdigit() and 8 <= len(test) <= 15:
                        try:
                            await msg.answer(text='Бот начал сбор данных, это может занять '
                                                  'от 20 секунд до 3х минут, пожалуйста, ожидайте.')
                            await msg.bot.send_chat_action(msg.chat.id, 'typing')
                            await asyncio.sleep(3)
                            await msg.answer(text="Если запрос идёт на юридическое лицо, то вам также "
                                                  "будет доступен PDF-файл, "
                                                  "в котором будет находиться вся подробная информация.")
                            await msg.bot.send_chat_action(msg.chat.id, 'typing')
                            inn = msg.text
                            info = parse.json_parse(inn)
                            try:
                                await msg.bot.send_chat_action(msg.chat.id, 'typing')
                                json_data = info[24]
                            except IndexError:
                                await msg.bot.send_chat_action(msg.chat.id, 'typing')
                                json_data = info[0]
                            try:
                                text = ''
                                if json_data['ФНС']['items'][0]['ИП']:
                                    text = parse.check_text_2(info)
                            except KeyError:
                                text = parse.check_text(info)
                            user_id = msg.from_user.id
                            u_id = await sqlite.get_id(user_id)
                            if json_data != {'message': 'Компания / ИП не найдены в ЕГРЮЛ / ЕГРИП (2)'}:
                                await mysql.update_log(user_id=u_id, data=inn, json_data=json_data)
                            await msg.answer(text=text)
                            try:
                                if json_data['ФНС']['items'][0]['ИП']:
                                    await msg.bot.send_chat_action(msg.chat.id, 'typing')
                                    await asyncio.sleep(3)
                                    await msg.answer("Чтобы проверить следующий ИНН/ОГРН, просто отправьте его в чат")
                            except (KeyError, TypeError):
                                await create_pdf(msg, inn)

                        except:
                            await msg.answer(text='По введенным данным нет информации, попробуйте ввести другие')
                    else:
                        await msg.answer(text='Неверный формат сообщения. Введите ИНН или ОГРН, '
                                              'используя только цифры (15 цифр максимум).')
                else:
                    await msg.answer('У вас закончился лимит проверок на месяц.')
            except TypeError:
                await msg.answer('У вас нет подписки!')


async def create_pdf(msg: types.Message, inn: str):
    await msg.bot.send_chat_action(msg.chat.id, 'typing')
    await asyncio.sleep(1)
    await msg.answer("Бот подготавливает полный отчет, пожалуйста, ожидайте.")
    await msg.bot.send_chat_action(msg.chat.id, 'upload_document')
    url = f"https://svoya-proverka.ru/v2/export-pdf.php?ogrn={inn}&" \
          f"blocks=[%221%22,%222%22,%224%22,%225%22,%226%22,%229%22]"
    response = requests.get(url)
    with open("example.pdf", "wb") as f:
        file = f.write(response.content)
    with open("example.pdf", "rb") as f:
        file_bytes = io.BytesIO(f.read())
        input_file = types.InputFile(file_bytes, f"Полный отчет_{inn}.pdf")
    await msg.bot.send_document(msg.from_user.id, document=input_file)
    await msg.bot.send_chat_action(msg.chat.id, 'typing')
    await asyncio.sleep(4)
    await msg.answer("Чтобы проверить следующий ИНН/ОГРН, просто отправьте его в чат")


def register(dp: Dispatcher):
    dp.register_message_handler(check_result, content_types="text")
    dp.register_callback_query_handler(create_pdf, text='get_pdf_file_txt')
