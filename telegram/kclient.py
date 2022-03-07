from os import getenv as env

from pyrogram import Client, filters

from classes.lib import turn_on
from telegram.msg_formatter import text_formatter


class Telegram(Client):

    katsu_id = 600432868
    config_id = -1001328058005
    username = "yoko_bridgebot"
    filters = filters
    formatter = text_formatter

    def __init__(self):
        super().__init__(
            "session/yoko", env("API_ID"), env("API_HASH"), bot_token=env("TG_TOKEN")
        )

    async def start(self):
        await super().start()

        self.bot = await turn_on(self)
        self.username = self.bot.username

    async def send_error(self, error, traceback):
        txt = (
            "**Error occured:**\n"
            f"\n**Bot:** @{self.username}"
            f"\n**Error:** ```{str(error)}```"
            f"\n**Traceback:** ```{str(traceback)}```"
        )

        self.send_message(self.config_id, txt)

    async def check_admin(self, msg):
        member = await self.get_chat_member(msg.chat.id, msg.from_user.id)
        if member.status in ("administrator", "creator"):
            return True
        if msg.from_user.id == self.katsu_id:
            return True
        return False
