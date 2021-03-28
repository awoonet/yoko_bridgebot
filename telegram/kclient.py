from pyrogram import Client, filters
from telegram.msg_formatter import text_formatter

class Telegram(Client):

	katsu_id	=  600432868
	config_id	= -1001328058005
	username	= 'yoko_bridgebot'
	filters		= filters
	formatter = text_formatter

	async def kstart(self):
		await self.start()

		self.bot = await self.get_me()
		self.username = self.bot.username

		txt = f'\n**Bot:** @{self.username}\n__Started work.__'
		self.send_message(self.config_id, txt)

	@staticmethod
	def to_discord(func):
		async def wrapper(app, msg):
			tg_id, dc_id, verified = await app.db.fetch_dc_id(msg.chat.id)

			print(f'Resent msg from {msg.chat.title}.')
			if dc_id and verified:
				chan = app.dc.get_channel(dc_id)
				txt  = await app.formatter(msg)

				await func(app, msg, chan, txt)
			
			await msg.continue_propagation()
		return wrapper	
	
	async def send_error(self, error, traceback):
		txt = ( '**Error occured:**\n'
						f'\n**Bot:** @{self.username}'
						f'\n**Error:** ```{str(error)}```'
						f'\n**Traceback:** ```{str(traceback)}```'
						)

		self.send_message(self.config_id, txt)