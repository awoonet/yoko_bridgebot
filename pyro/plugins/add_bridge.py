import logging
from pyrogram.types import Message
from pyro.client import Telegram as app

f = app.filters


@app.on_message(f.group & f.command(["add_bridge"]) & ~f.edited & ~f.user("me"))
@app.error_catcher
async def add_bridge(app, msg: Message):
    conditions = (
        (await app.check_admin(msg), "telegram.error.establish"),
        (len(msg.command) == 2, "telegram.error.no_id"),
        (
            app.dc.get_channel(int(msg.command[1])) is not None,
            "telegram.error.failed.id",
        ),
    )

    condition = True
    async for i in conditions:
        if not i[0]:
            condition = i[0]
            response = app.t(i[1])

    if condition:
        logging.warning(
            f"tg={msg.chat.id} type={type(msg.chat.id)}, dc={msg.command[1]} type={type(msg.command[1])}"
        )
        await app.db.add_chat(msg.chat.id, msg.command[1])

        response = app.t("discord.verify", msg.chat.title)
        await app.dc.send_message(int(msg.command[1]), response)

        response = app.t("telegram.ok_id")

    await msg.reply(response)
