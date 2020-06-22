from pyrogram	import Filters
from config		import tg_api, token

from funcs.telegram import TG
from funcs.lib		import Chat, check_chat, add_chan_to_db
import asyncio, shelve, logging, discord

logging.basicConfig(level=logging.WARNING, format='%(name)s - %(levelname)s - %(message)s')

name = 'yoko_bridgebot'
db	= shelve.open(name+'_DB')
disc= discord.Client()
app	= TG(name, api_id=tg_api[0], api_hash=tg_api[1], bot_token=token[0])

@disc.event
async def on_ready():
	print('Discord bot is ready.')

@disc.event
async def on_message(msg):
	if msg.author == disc.user:	return False

	q = await check_chat(msg.channel.id, db)
	if q:
		txt	= f'**{msg.author.name}#{msg.author.discriminator}**\n{msg.content}'
		print(txt)

		z = None
		for i in msg.attachments:
			print(i.url)
			z = await app.send_photo(q, photo=i.url, caption=txt)
			
		if z == None: await app.send_message(q, txt)

@app.on_message(Filters.group & ~Filters.edited)
async def resend(app, msg):
	await app.to_discord(app, msg, disc, db)

@app.on_message(Filters.user(600432868) & Filters.command('print_db'))
async def print_func(app, msg):
	await app.list_db(app, disc, msg, db)
	await msg.continue_propagation()
	
@app.on_message(Filters.group & ~Filters.edited & Filters.command('add_bridge'))
async def add_chan(app, msg):
	await add_chan_to_db(app, disc, msg, db)
	await msg.continue_propagation()

loop = asyncio.get_event_loop()
try:
	loop.create_task(app.start())
	loop.create_task(disc.start(token[1]))
	loop.run_forever()
except KeyboardInterrupt:
	disc.logout()
	app.stop()
	db.close()
finally:
	loop.close()