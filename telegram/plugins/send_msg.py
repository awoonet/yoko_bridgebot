from telegram.kclient import Telegram as app
from os 							import remove
from discord					import File

f = app.filters

def is_animated(filter, app, msg):
	if msg.sticker is not None:
		return msg.sticker.is_animated

def to_discord(func):
	async def wrapper(app, msg):
		tg_id, dc_id, verified = await app.db.fetch_dc_id(msg.chat.id)

		if verified:
			await func(app, msg, 
										app.dc.get_channel(dc_id), 
										await app.formatter(msg))
		
		await msg.continue_propagation()
	return wrapper	

@app.on_message(f.group & f.media & ~f.edited & ~f.user('me') & ~f.create(is_animated))
@to_discord
async def media(app, msg, chan, txt):	
	file = await msg.download()
	await chan.send(content=txt[0], embed=txt[1], file=File(fp=file))
	remove(file)

@app.on_message(f.group & f.text & ~f.edited & ~f.user('me'))
@to_discord
async def text(app, msg, chan, txt):	
	await chan.send(content=txt[0], embed=txt[1])