from telegram.kclient import Telegram as app

f = app.filters


@app.on_message(f.group & f.command(["add_bridge"]) & ~f.edited & ~f.user("me"))
async def add_bridge(app, msg):
    conditions = (
        (
            await app.check_admin(msg),
            "Тебе нужно быть администратором, чтобы прокидывать мосты.",
        ),
        (
            len(msg.command) == 2,
            "Напиши ID discord-чата после команды, с которым хочешь установить мост.",
        ),
        (
            app.dc.get_channel(int(msg.command[1])) is not None,
            "ID discord-чата не верный, пожалуйста, перепроверь и попробуй еще раз.",
        ),
    )

    condition = True
    async for i in conditions:
        if not i[0]:
            condition = i[0]
            answer = i[1]

    if condition:
        print(
            f"tg={msg.chat.id} type={type(msg.chat.id)}, dc={msg.command[1]} type={type(msg.command[1])}"
        )
        await app.db.add_chat(msg.chat.id, msg.command[1])

        answer_dc = f"В этот чат проложен мост из телеграм чата {msg.chat.title}.\nПодтвердите, пожалуйста, написав: verify_bridge"
        await app.dc.send_message(int(msg.command[1]), answer_dc)
        answer = "ID discord-чата верный. Перейдите в дискорд и подтвердите установку соединения."

    await msg.reply(answer)
