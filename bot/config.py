import logging

from decouple import config

from bot.handlers.commands import register as reg_commands
from bot.handlers.states.login import register as reg_states_login
from bot.handlers.states.logout import register as reg_states_logout

bot_token = config('BOT_TOKEN')
logger = logging.getLogger(__name__)


def register_handlers(dp):
    reg_commands(dp)
    reg_states_login(dp)
    reg_states_logout(dp)
