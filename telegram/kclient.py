from os import getenv as env

from pyrogram import Client, filters
from pyrogram.types import Message

from classes.lib import turn_on
from telegram.msg_formatter import text_formatter


class Telegram(Client):

    katsu_id = 600432868
    config_id = -1001328058005
    username = "yoko_bridgebot"
    filters = filters
    formatter = text_formatter

    async def kstart(self):
        await self.start()

        self.bot = await self.get_me()
        await turn_on(self)
        self.username = self.bot.username

    async def send_error(self, error, traceback) -> str:
        txt = (
            "**Error occured:**\n"
            f"\n**Bot:** @{self.username}"
            f"\n**Error:** ```{str(error)}```"
            f"\n**Traceback:** ```{str(traceback)}```"
        )

        self.send_message(self.config_id, txt)

    async def check_admin(self, msg: Message) -> bool:
        member = await self.get_chat_member(msg.chat.id, msg.from_user.id)
        admin_status = ("administrator", "creator")

        member.status in admin_status or msg.from_user.id == self.katsu_id
