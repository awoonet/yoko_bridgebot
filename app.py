from os import getenv as env
import asyncio, logging, traceback
from dotenv import load_dotenv

from telegram.kclient import Telegram as app
from discord.kclient import Discord as disc
from classes.psql import Database as psql

load_dotenv()

db = psql()
dc = disc()
tg = app("session/yoko", env("API_ID"), env("API_HASH"), bot_token=env("TG_TOKEN"))


async def main():
    try:
        await db.init_table()

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


# if __name__ == "__main__":
#     # tg.run(main(tg, dc, db))


#     tg.db, dc.db = db, db
#     tg.dc, dc.tg = dc, tg
#     loop = asyncio.new_event_loop()
#     # task = asyncio.gather(db.init_table(), dc.start(env("DC_TOKEN")), tg.start())
#     # loop.run_until_complete(task)

#     loop.create_task(dc.start(env("DC_TOKEN")))
#     loop.create_task(tg.kstart())
#     loop.create_task(db.init_table())
#     loop.run_forever()
