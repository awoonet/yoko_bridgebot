from telegram.kclient import Telegram as app

f = app.filters
@app.on_message(f.group & f.text & ~f.edited & ~f.user('me'))
@app.to_discord
async def text(app, msg, chan, txt):	
	await chan.send(txt)