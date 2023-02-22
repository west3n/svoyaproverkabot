from aiogram import Dispatcher, types

from bot.database.mysql import mysql
from bot.database.sqlite import sqlite
from bot.keyboards import inline

import json


async def bot_start(msg: types.Message):
    user_name = msg.from_user.first_name
    user_id = msg.from_user.id
    user = await sqlite.user_status(user_id)
    if not user:
        await msg.answer(text=f'Привет, {user_name}! Вы не вошли в аккаунт!',
                         reply_markup=inline.login())
    else:
        bot_db = await sqlite.get_id(user_id)
        display_name = await sqlite.get_display_name(user_id)
        result = await mysql.get_user_profile(bot_db[0])
        date = result[1].strftime("%d.%m.%Y")
        count = await mysql.count_scoring(bot_db[0])
        await msg.answer(f"\n<b>Ваш профиль:</b>"
                         f'\n✅<em>Добро пожаловать, <b>{display_name}!</b></em>'
                         f"\n🌐<em>Ваш тариф:</em><b> {result[0]} </b>"
                         f"\n📅<em>Действует до:</em> <b>{date}</b>"
                         f"\n📝<em>Осталось проверок:</em><b> {result[2] - count}</b>\n\n",
                         reply_markup=inline.logout())
        await msg.answer(f"📑 Чтобы проверить организацию введите ИНН или ОГРН организации")


async def history(msg: types.Message):
    user_id = msg.from_user.id
    user = await sqlite.user_status(user_id)
    if user:
        await msg.delete()
        await msg.answer('<b>Загружаю последние 5 проверок, ожидайте</b>')
        u_id = await sqlite.get_id(user_id)
        logs = await mysql.check_log(u_id[0])
        counter = 0
        for log in logs:
            if counter >= 5:
                break
            date = log[2]
            ogrn = log[3]
            org_json = json.loads(log[4])
            org_name = org_json["ФНС"]["items"][0]["ЮЛ"]["НаимСокрЮЛ"]
            counter += 1
            await msg.answer(text=f'<em>Дата проверки</em>: <b>{date.strftime("%d.%m.%Y")}</b>\n'
                                  f'<em>ИНН/ОГРН:</em><b><a href="'
                                  f'https://svoya-proverka.ru/scoring/?ogrn={ogrn}"> {ogrn}</a></b>\n'
                                  f'<em>Организация:</em> <b>{org_name}</b>')
        await msg.answer(
            '<b>Полную историю вы можете посмотреть <a href="https://svoya-proverka.ru/cabinet/">на сайте</a> в '
            'личном кабинете</b>')
    else:
        await msg.answer(f'Вы не вошли в профиль!\n'
                         f'Для входа используйте /login')


def register(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands='start', state='*')
    dp.register_message_handler(history, commands='history')
