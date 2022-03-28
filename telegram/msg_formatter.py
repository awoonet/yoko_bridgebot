from pyrogram.types import Message
from discord import Embed
import re


async def fetch_text(msg: Message) -> str:
    if msg.text is not None:
        return msg.text.markdown.replace("__", "_")
    elif msg.caption is not None:
        return msg.caption.markdown.replace("__", "_")
    else:
        return ""


async def fetch_name(msg: Message) -> str:
    if msg.from_user is not None:
        user = msg.from_user
    elif msg.forward_from is not None:
        user = msg.forward_from
    elif msg.sender_chat is not None:
        return msg.sender_chat.title

    if user.last_name is not None:
        return f"{user.first_name} {user.last_name}"
    else:
        return user.first_name


async def forwarded(msg: Message) -> str:
    if msg.forward_from_chat is not None:
        title = msg.forward_from_chat.title
        return f"\n**Переслано из канала: {title}**\n"

    if msg.forward_from is not None:
        name = await fetch_name(msg)
    elif msg.forward_sender_name is not None:
        name = msg.forward_sender_name
    else:
        return ""

    return f"\n**Переслано от пользователя: {name}**\n"


async def format_msg(msg: Message) -> str:
    name = await fetch_name(msg)
    text = await fetch_text(msg)
    fwd = await forwarded(msg)
    return f"**{name}:** {fwd}{text}"


async def reply_msg(msg: Message) -> str:
    reply_not_none = msg.reply_to_message is not None

    if reply_not_none:
        text = await format_msg(msg.reply_to_message)
        return f"В ответ на сообщение:\n{text}\n\n"
    return reply_not_none


async def guess_for_embed(msg: Message) -> tuple:
    to_embed = ""

    msg_text = await format_msg(msg)
    if re.search(r"\[.+\]\(.+\)", msg_text):
        to_embed = msg_text
        content = None
    else:
        content = msg_text

    reply = await reply_msg(msg)
    if reply:
        to_embed += reply

    return (content, to_embed)


async def make_embed_discord(text: str) -> Embed | None:
    embed = None
    if text:
        embed = Embed()
        embed.description = text
    return embed


async def text_formatter(self, msg: Message) -> tuple:
    content, to_embed = await guess_for_embed(msg)
    embed = await make_embed_discord(to_embed)

    return (content, embed)
