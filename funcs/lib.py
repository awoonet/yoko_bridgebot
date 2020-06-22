import traceback

class Chat:
	def __init__(self, discord, telegram):
		self.d_id	= discord
		self.t_id	= telegram

	async def update(self, app, disc):
		chan = disc.get_channel(self.d_id)
		chat = await app.get_chat(self.t_id)

		self.d_name	= chan.name
		self.t_name	= chat.title
		print(await self.chat(app, disc))
		
	async def chat(self, app, disc):
		t = self.t_name
		d = self.d_name
		return f'`{t} - {d}`'


async def check_chat(chat_id, db):
	chat_id = int(chat_id)
	for y in db.values():
		if   chat_id == int(y.t_id):	return y.d_id
		elif chat_id == int(y.d_id):	return y.t_id
		else:					pass
	return False
	
async def add_chan_to_db(app, disc, msg, db):
	txt = False
	cid, uid = str(msg.chat.id), msg.from_user.id

	if cid not in db.keys():
		s = await app.get_chat_member(cid, uid) 

		if s.status == 'owner' or uid == 600432868:
			try:
				d_id = int(msg.text.split()[1])

				chan = disc.get_channel(d_id)
				await chan.send(f'Установлен мост с чатом **{msg.chat.title}**')
	
				db[str(cid)] = Chat(d_id, cid)
				await db[str(cid)].update(app, disc)

				txt = f'Установлен мост с чатом **{chan.name}** на сервере **{chan.guild.name}**'
			
			except Exception as e:	
				await app.send_message(-1001328058005, f'@yoko_bridgebot\n{e}\n{traceback.format_exc()}')
				txt = 'Не удалось установить мост.'			
		else: 
			txt = 'Тебе надо быть владельцем чата!'
	else: 
		txt = 'Чат уже есть в базе данных.'
	
	if txt: await msg.reply(txt)

	db.sync()