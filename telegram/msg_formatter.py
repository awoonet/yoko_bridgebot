from discord import Embed
import re


async def fetch_text(msg):
    """Возвращает caption, text или ничего из сообщения"""
    if msg.text is not None:
        return msg.text.markdown.replace("__", "_")
    elif msg.caption is not None:
        return msg.caption.markdown.replace("__", "_")
    else:
        return ""


async def fetch_name(msg):
    """Возвращает username, имя с фамилией или просто имя
    отформатированное в соответствии с полученной командой."""
    if msg.from_user is not None:
        user = msg.from_user
        if user.last_name is not None:
            return f"{user.first_name} {user.last_name}"
        else:
            return user.first_name
    elif msg.sender_chat is not None:
        return msg.sender_chat.title


async def forwarded(msg):
    answer = ""
    if msg.forward_from is not None:
        answer = f"от пользователя: {await fetch_name(msg.forward_from)}"
    elif msg.forward_sender_name is not None:
        answer = f"от пользователя: {msg.forward_sender_name}"
    elif msg.forward_from_chat is not None:
        answer = f"из канала: {msg.forward_from_chat.title}"
    return f"\n**Переслано {answer}**\n" if answer else ""


async def format_msg(msg):
    name = await fetch_name(msg)
    text = await fetch_text(msg)
    fwd = await forwarded(msg)
    return f"**{name}:** {fwd}{text}"


async def reply_msg(msg):
    if msg.reply_to_message is not None:
        text = await format_msg(msg.reply_to_message)
        return f"В ответ на сообщение:\n{text}\n\n"
    return ""


async def text_formatter(self, msg):
    rpl = await reply_msg(msg)
    msg = await format_msg(msg)

    content, to_embed = "", ""

    if re.search(r"\[.+\]\(.+\)", msg):
        to_embed += msg
        content = None
    else:
        content += msg

    if rpl:
        to_embed += rpl

    if to_embed:
        embed = Embed()
        embed.description = to_embed
    else:
        embed = None

    return (content, embed)
