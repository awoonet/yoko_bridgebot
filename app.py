from os import getenv as env
import asyncio, logging, coloredlogs

from dotenv import load_dotenv

from pyro.client import Telegram as pyro
from disc.client import Discord as disc
from db.psql import Database as psql
from functions.load_i18n import load_i18n

load_dotenv()
coloredlogs.install()
logging.basicConfig(level=logging.INFO)

t = load_i18n()
db = psql(t)
dc = disc(t, db)
tg = pyro(t, db)

tg.dc, dc.tg = dc, tg

try:
    loop = asyncio.get_event_loop()
    # loop.create_task(main())
    loop.create_task(db.init_table())
    loop.create_task(tg.start())
    loop.create_task(dc.start(env("DC_TOKEN")))
    loop.run_forever()

except KeyboardInterrupt:
    loop.run_until_complete(tg.stop())
    loop.run_until_complete(dc.logout())
    loop.run_until_complete(db.close())
    loop.stop()

finally:
    loop.close()
