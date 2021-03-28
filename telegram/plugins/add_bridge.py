from telegram.kclient import Telegram as app

@app.on_message(app.filters.group & app.filters.command(['add_bridge', f'add_bridge@{app.username}']) & ~app.filters.edited)
async def add_bridge(app, msg):
	is_katsu = msg.from_user.id == app.katsu_id
	is_admin = (await app.get_chat_member(msg.chat.id, msg.from_user.id)).status in ('administrator', 'creator')

	if is_katsu or is_admin:
		if len(msg.command) == 2:
			chan = app.dc.get_channel(int(msg.command[1]))
			
			if chan is not None:
				answer = 'ID discord-чата верный. Добавляем в базу данных.'
				await app.db.add_chat(msg.chat.id, msg.command[1])
				await chan.send(f'В этот чат проложен мост из телеграм чата {msg.chat.title}.\nПодтвердите, пожалуйста, написав: verify_bridge')
			else:
				answer = 'ID discord-чата не верный, пожалуйста, перепроверь и попробуй еще раз.'
		else:
			answer = 'Напиши ID discord-чата после команды, с которым хочешь установить мост.'
	else:
		answer = 'Тебе нужно быть администратором, чтобы прокидывать мосты.'

	await msg.reply(answer)