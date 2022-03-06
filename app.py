from os import getenv as env
from dotenv import load_dotenv

from telegram.kclient import Telegram as app
from discord.kclient import Discord as disc
from classes.psql import Database as psql
import classes, asyncio, logging, traceback

load_dotenv()
db = psql()
dc = disc()
tg = app("session/yoko", env("API_ID"), env("API_HASH"), bot_token=env("TG_TOKEN"))


async def main():
    try:
        await db.init_table()
        logging.warning("DB connection open!")

        tg.db, dc.db = db, db
        tg.dc, dc.tg = dc, tg

        await tg.kstart()
        await dc.start(env("DC_TOKEN"))

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
