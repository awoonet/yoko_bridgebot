from os import remove
from collections.abc import Callable
from pyrogram.types import Message
from pyro.client import Telegram as app
from discord import File

f = app.filters


def is_animated(filter, app: app, msg: Message):
    if msg.sticker is not None:
        return msg.sticker.is_animated


def to_discord(func: Callable) -> Callable:
    async def wrapper(app: app, msg: Message):
        _, dc_id, verified = await app.db.fetch_dc_id(msg.chat.id)
        if verified:
            chan = app.dc.get_channel(int(dc_id))
            msg_text = await app.formatter(msg)

            await func(app, msg, chan, msg_text)

    return wrapper


@app.on_message(f.group & f.media & ~f.edited & ~f.user("me") & ~f.create(is_animated))
@app.error_catcher
@to_discord
async def media(_: app, msg: Message, chan, txt):
    file = await msg.download()
    await chan.send(content=txt[0], embed=txt[1], file=File(fp=file))
    remove(file)


@app.on_message(f.group & f.text & ~f.edited & ~f.user("me"))
@app.error_catcher
@to_discord
async def text(_: app, __: Message, chan, txt):
    await chan.send(content=txt[0], embed=txt[1])
