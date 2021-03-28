import discord, mimetypes

class Discord(discord.Client):
	katsu_id = 435531611543437312
	
	async def on_message(self, msg):
		if msg.author == self.user:	
			return False			

		else:
			app = self.tg
			tg_id, dc_id, verified = await app.db.fetch_tg_id(msg.channel.id)

			if tg_id and verified:
				txt	= f'**{msg.author}**\n{msg.content}'
									
				if msg.content:
					await app.send_message(tg_id, txt)
				else:
					media_url = msg.attachments[0].url
					await self.send_media(tg_id, media_url, txt)								
			elif tg_id:
				await self.add_bridge(self, self.db, msg)

	async def add_bridge(disc, db, msg):
		chan = disc.get_channel(msg.channel.id)

		is_owner = msg.author.id == chan.guild.owner_id
		is_katsu = msg.author.id == self.katsu_id

		if is_owner or is_katsu:

			if 'verify_bridge' in msg.content:
				await db.verify_chat(msg.channel.id)
				answer = 'Подтверждено, мост проложен.'
			else:
				answer = "Подтвердите, пожалуйста, написав: verify_bridge"
		else:
			answer = "Нужно быть владельцем сервера, чтобы подтвердить установку моста."

		await chan.send(answer)
	
	async def send_media(self, chat_id, url, txt):
		app = self.tg
		media_type = (mimetypes.guess_type(url=url))[0]

		if 	 'gif' 	 in media_type: await app.send_animation(	chat_id, animation=url, caption=txt)
		elif 'image' in media_type: await app.send_photo(			chat_id, photo		=url,	caption=txt)
		elif 'audio' in media_type: await app.send_audio(			chat_id, audio		=url,	caption=txt)
		elif 'video' in media_type: await app.send_video(			chat_id, video		=url,	caption=txt)	
		else:												await app.send_document(	chat_id, document	=url,	caption=txt)