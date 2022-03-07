from os import getenv as env
from dotenv import load_dotenv

from telegram.kclient import Telegram as app
from discord.kclient import Discord as disc
from classes.psql import Database as psql
import classes, asyncio, logging, traceback

load_dotenv()


async def main(tg, dc, db):
    try:
        await db.init_table()
        await tg.start()
        await dc.start(env("DC_TOKEN"))
    except KeyboardInterrupt:
        await dc.logout()
        await tg.stop()
        await db.close()
    except Exception as e:
        tg.send_error(e, traceback.format_exc())
        logging.exception("Exception occurred")


if __name__ == "__main__":

    db = psql()
    dc = disc()
    tg = app()

    tg.db, dc.db = db, db
    tg.dc, dc.tg = dc, tg

    asyncio.run(main(tg, dc, db))
