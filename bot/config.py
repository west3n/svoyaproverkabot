import logging

from decouple import config

from bot.handlers.commands import register as reg_commands
from bot.handlers.states.registration import register as reg_states


bot_token = config('BOT_TOKEN')
logger = logging.getLogger(__name__)


def register_handlers(dp):
    reg_commands(dp)
    reg_states(dp)
