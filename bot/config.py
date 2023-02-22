import logging

from aiogram import types
from decouple import config

from bot.handlers.commands import register as reg_commands
from bot.handlers.states.login import register as reg_states_login
from bot.handlers.states.logout import register as reg_states_logout
from bot.handlers.text_content import register as reg_text_content

bot_token = config('BOT_TOKEN')
logger = logging.getLogger(__name__)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Начало работы с ботом"),
        types.BotCommand("history", "Последние пять проверок")
    ])


def register_handlers(dp):
    reg_commands(dp)
    reg_states_login(dp)
    reg_states_logout(dp)
    reg_text_content(dp)
