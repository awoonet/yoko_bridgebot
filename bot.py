from telegram.kclient	import Telegram as app
from discord.kclient	import Discord	as disc
from classes.sqlite		import Database as sqlite
from os import getenv as env
import classes, asyncio, logging, traceback


db = sqlite('DB/yoko.db')
dc = disc()
tg = app('yoko', env('API_ID'), env('API_HASH'), bot_token=env('TG_TOKEN'))

async def main():
	try:
		await db.init_table()
		logging.warning("DB connection open!")

		tg.db, dc.db = db, db
		tg.dc, dc.tg = dc, tg

		await tg.kstart()
		await dc.start(env('DC_TOKEN'))

	except Exception as e:
		tg.send_error(e, traceback.format_exc())
		logging.exception("Exception occurred")

try:
	loop = asyncio.get_event_loop()
	loop.create_task(main())
	loop.run_forever()

except KeyboardInterrupt:
	loop.run_until_complete(tg.stop())
	loop.run_until_complete(dc.logout())
	loop.run_until_complete(db.close())
	loop.stop()
	
finally:
	loop.close()