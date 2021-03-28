from telegram.kclient import Telegram as app
from discord 					import File
from os 							import remove


f = app.filters
@app.on_message(f.group & f.media & ~f.edited & ~f.user('me'))
@app.to_discord
async def media(app, msg, chan, txt):	
	file = await msg.download()
	await chan.send(txt, file=File(fp=file))
	remove(file)

