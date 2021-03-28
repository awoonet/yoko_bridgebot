import discord, logging 

class Discord(discord.Client):
	katsu_id = 435531611543437312
	
	async def on_message(self, msg):
		if msg.author == self.user:	return 			

		tg_id, dc_id, verified = await self.db.fetch_tg_id(msg.channel.id)

		if verified:
				txt	= f'**{msg.author}**\n{msg.content}'			
				if msg.content:
					await app.send_message(tg_id, txt)
				else:
					media_url = msg.attachments[0].url
					await self.send_media(tg_id, media_url, txt)
		else:
			await self.add_bridge(self, self.db, msg)

	async def add_bridge(self, disc, db, msg):
		conditions = (
			(await self.check_admin(msg), 	'Тебе нужно быть администратором, чтобы подтвердить установку моста.'),
			('verify_bridge' in msg.content,'Подтвердите, пожалуйста, установку моста, написав: verify_bridge'),
		)

		condition = True
		for i in conditions:
			if not i[0]:
				condition = i[0]
				answer = i[1]

		if condition:
				await db.verify_chat(msg.channel.id)
				answer = 'Подтверждено, мост проложен.'

		await self.send_message(msg.channel.id, answer)

	async def send_message(self, chat_id: int, txt: str, file=None):
		if file is not None:	
			file = discord.File(fp=file)
		else:			
			await self.get_channel(chat_id).send(content=txt, file=file)

	async def check_admin(self, msg):
		if msg.author.guild_permissions.administrator: return True
		if msg.author.id == self.katsu_id: return True
		return False
	
	async def send_media(self, chat_id: int, url: str, txt: str):
		app = self.tg
		media_type = (mimetypes.guess_type(url=url))[0]

		if 	 'gif' 	 in media_type: await app.send_animation(	chat_id, animation=url, caption=txt)
		elif 'image' in media_type: await app.send_photo(			chat_id, photo		=url,	caption=txt)
		elif 'audio' in media_type: await app.send_audio(			chat_id, audio		=url,	caption=txt)
		elif 'video' in media_type: await app.send_video(			chat_id, video		=url,	caption=txt)	
		else:												await app.send_document(	chat_id, document	=url,	caption=txt)
