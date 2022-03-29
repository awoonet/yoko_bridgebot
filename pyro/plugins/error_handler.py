import traceback
from typing import Callable
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

not_none = lambda x: x is not None


class ErrorHandler:
    """
    Helper class for send messages if handled
    """

    @staticmethod
    def error_catcher(func: Callable) -> Callable:
        async def wrapper(app, msg) -> None:
            try:
                return await func(app, msg)
            except Exception as e:
                await app.send_error_msg(msg, e)

            await msg.continue_propagation()

        return wrapper

    async def send_error_msg(self, msg, error: Exception) -> None:
        tg_message = isinstance(msg, Message)
        to_chat = int(self.config_id)
        error = str(error)

        method = self.prepare_tg_msg if tg_message else self.prepare_dc_msg

        txt = await self.prepare_error_msg(await method(msg), error)
        kb = await self.prepare_error_keyboard(error)

        await self.send_message(to_chat, txt, reply_markup=kb)
        if tg_message:
            await self.forward_messages(to_chat, msg.chat.id, (msg.message_id,))

    async def prepare_error_msg(self, message, error) -> str:
        return (
            "**Error occured in message:**\n\n"
            f"{message}\n\n"
            f"**Error:** ```{str(error)}```\n"
            f"**Traceback:** ```{str(traceback.format_exc())}```"
        )

    async def prepare_error_keyboard(self, error):
        error = str(error).replace(" ", "+")
        services = {
            "Google": "www.google",
            "StackOverflow": "stackoverflow",
            "StackExchange": "stackexchange",
        }

        row = [
            InlineKeyboardButton(
                text=title, url=f"https://{link}.com/search?q=python+{error}"
            )
            for title, link in services.items()
        ]

        return InlineKeyboardMarkup([row])

    async def prepare_tg_msg(self, msg) -> str:
        user = msg.from_user

        txt = (
            f"**Bot:** __@{self.bot.username}__"
            f"\n**Chat:** __{msg.chat.title}__"
            f"\n**Chat ID:** __{msg.chat.id}__** / **__{msg.message_id}__"
            f"\n**User:** __{user.first_name} __"
            f" __{user.last_name if not_none(user.last_name) else ''}__"
            f" __(@{user.username if not_none(user.username) else ''})__"
            f"\n**User ID:** __{user.id}__"
            f"\n**Text:** {msg.text.html if not_none(msg.text) else ''}"
        )

        if not_none(msg.media) and msg.media:
            msg_types = {
                "Audio": msg.audio,
                "Document": msg.document,
                "Photo": msg.photo,
                "Sticker": msg.sticker,
                "Animation": msg.animation,
                "Video": msg.video,
                "Voice": msg.voice,
                "Video note": msg.video_note,
            }
            for name, msg_type in msg_types:
                if not_none(msg_type):
                    txt += f"\n**{name}**:_{msg_type.file_id}__"

            txt += f"\n**Caption**:__{msg.caption}__" if not_none(msg.caption) else ""

        return txt

    async def prepare_dc_msg(self, msg) -> str:
        user = msg.author
        txt = f"**Bot:** __{self.dc.user}__"
        if not_none(msg.guild):
            txt += f"\n**Guild: __{msg.guild} ({msg.guild.id})__"
        if not_none(msg.channel):
            txt += f"\n**Channel:** __{msg.channel.name} ({msg.channel.id})__"
        txt += (
            f"\n**User name:** __{user.name} ({user.id})__"
            f"\n**User nick:** __{user.nick if not_none(user.nick) else 'none'}__"
            f"\n**Content:** {msg.content if not_none(msg.content) else 'none'}"
            f"\n**Embeds:** {msg.embeds if not_none(msg.embeds) else 'none'}"
        )

        return txt
