import logging, traceback
from os import getenv as env

from pyrogram import Client, filters
from pyrogram.types import Message

from pyro.plugins.send_awaking import turn_on
from pyro.plugins.msg_formatter import text_formatter
from pyro.plugins.error_handler import ErrorHandler


class Telegram(Client, ErrorHandler):

    katsu_id = 600432868
    config_id = -1001328058005
    username = "yoko_bridgebot"
    filters = filters
    formatter = text_formatter

    def __init__(self):
        super().__init__(
            "session/yoko",
            env("API_ID"),
            env("API_HASH"),
            bot_token=env("TG_TOKEN"),
            plugins={"root": "pyro"},
        )

    async def start(self):
        await super().start()

        self.bot = await self.get_me()
        await turn_on(self)
        self.username = self.bot.username

        logging.warning(f" Telegram bot started as @{self.bot.username}")

    async def check_admin(self, msg: Message) -> bool:
        member = await self.get_chat_member(msg.chat.id, msg.from_user.id)
        admin_status = ("administrator", "creator")

        member.status in admin_status or msg.from_user.id == self.katsu_id
