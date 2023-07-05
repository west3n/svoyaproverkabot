from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from bot import config
from bot.database.mysql import mysql
from bot.database.sqlite import sqlite
from bot.keyboards import inline, reply
from bot import states as st
import json
from mysql.connector.errors import InternalError


async def bot_start(msg: types.Message):
    if msg.chat.type == 'private':
        user_name = msg.from_user.first_name
        user_id = msg.from_user.id
        user = await sqlite.user_status(user_id)
        if not user:
            await msg.answer(text=f'Привет, {user_name}! Вы не вошли в аккаунт!',
                             reply_markup=inline.login())
        else:
            try:
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
                await msg.answer(f"📑 Чтобы проверить организацию, введите её ИНН или ОГРН:")
            except TypeError:
                display_name = await sqlite.get_display_name(user_id)
                await msg.answer(f"\n<b>Ваш профиль:</b>"
                                 f'\n✅<em>Добро пожаловать, <b>{display_name}!</b></em>\n\n'
                                 f'У вас нет оформленной подписки!', reply_markup=inline.logout())
            except InternalError:
                display_name = await sqlite.get_display_name(user_id)
                await msg.answer(f"\n<b>Ваш профиль:</b>"
                                 f'\n✅<em>Добро пожаловать, <b>{display_name}!</b></em>\n\n'
                                 f'У вас нет оформленной подписки!', reply_markup=inline.logout())


async def history(msg: types.Message):
    if msg.chat.type == 'private':
        user_id = msg.from_user.id
        user = await sqlite.user_status(user_id)
        try:
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
                    try:
                        org_name = org_json["ФНС"]["items"][0]["ЮЛ"]["НаимСокрЮЛ"]
                    except KeyError:
                        org_name = org_json["ФНС"]["items"][0]["ИП"]["ФИОПолн"]
                    counter += 1
                    await msg.answer(text=f'<em>Дата проверки</em>: <b>{date.strftime("%d.%m.%Y")}</b>\n'
                                          f'<em>ИНН/ОГРН:</em><b><a href="'
                                          f'https://svoya-proverka.ru/scoring/?ogrn={ogrn}"> {ogrn}</a></b>\n'
                                          f'<em>Организация:</em> <b>{org_name}</b>')
                await msg.answer(
                    '<b>Полную историю вы можете посмотреть '
                    '<a href="https://svoya-proverka.ru/cabinet/">на сайте</a> в личном кабинете</b>')
            else:
                await msg.answer(f'Вы не вошли в профиль!\n'
                                 f'Для входа используйте /start')
        except InternalError:
            await msg.answer(f'У вас нет оформленной подписки!')

        except TypeError:
            await msg.answer(f'У вас нет оформленной подписки!')


async def tech_sup(msg: types.Message):
    if msg.chat.type == 'private':
        await msg.answer("Напишите ваш вопрос, он будет передан в службу поддержки", reply_markup=reply.cmd_cancel())
        await st.Support.info.set()


async def tech_sup_text(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data = {"text": msg.text, "user_name": msg.from_user.username, "user_id": msg.from_user.id}
    await msg.reply("Ваш вопрос передан в службу поддержки",
                    reply_markup=reply.remove)
    text = data['text']
    user_name = data['user_name']
    user_id = data['user_id']
    x = await sqlite.get_id(user_id)
    if x:
        email_full_name = await mysql.get_user_email_full_name(x[0])
        try:
            email = email_full_name[0]
        except TypeError:
            email = 'Нет данных'
        try:
            full_name = email_full_name[1]
        except TypeError:
            full_name = 'Нет данных'
        try:
            phone = await mysql.get_user_phone(x[0])
            phone = phone[0]
        except TypeError:
            phone = 'Нет данных'
        try:
            org = await mysql.get_user_org(x[0])
            org = org[0]
        except TypeError:
            org = 'Нет данных'

        await msg.bot.send_message(config.group_id, f"<b>Вопрос от пользователя @{user_name}</b>\n"
                                                    f"ИМЯ: {full_name}\n"
                                                    f"EMAIL: {email}\n"
                                                    f"ТЕЛЕФОН: {phone}\n"
                                                    f"ОРГАНИЗАЦИЯ: {org}"

                                                    f"\n\nВОПРОС: {text}",

                                   reply_markup=inline.sup_answer(user_name))
        await state.finish()

    else:
        await msg.bot.send_message(config.group_id, f"<b>Вопрос от пользователя @{user_name} (пользователь не "
                                                    f"вошел в аккаунт в боте)</b>\n"

                                                    f"\nВОПРОС: {text}",

                                   reply_markup=inline.sup_answer(user_name))


async def cmd_cancel(msg: types.Message, state: FSMContext):
    await msg.answer(text='Вы отменили действие!',
                     reply_markup=reply.remove)
    await state.finish()


async def sup_1(call: types.CallbackQuery):
    await call.message.edit_reply_markup()


def register(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, text='Отмена', state="*")
    dp.register_message_handler(bot_start, commands='start', state='*')
    dp.register_message_handler(history, commands='history')
    dp.register_message_handler(tech_sup, commands='help')
    dp.register_message_handler(tech_sup_text, state=st.Support.info)
    dp.register_callback_query_handler(sup_1, text='sup_1')
