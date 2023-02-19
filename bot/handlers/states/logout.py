from aiogram import Dispatcher, types
from bot.database.sqlite import sqlite
from bot.keyboards import inline


async def logout_verify(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(text='Вы точно хотите выйти из аккаунта?',
                              reply_markup=inline.confirm_logout())


async def cancel_logout(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Выход отменен. Посмотреть свой профиль - /profile')


async def logout(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(text='Вы вышли из аккаунта. Возвращайтесь скорее!')
    user_id = call.from_user.id
    await sqlite.delete_user(user_id)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(logout_verify, text='logout_verify')
    dp.register_callback_query_handler(cancel_logout, text='cancel_logout')
    dp.register_callback_query_handler(logout, text='logout')
