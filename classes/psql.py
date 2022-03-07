from os import getenv as env
import logging, psycopg2
import urllib.parse as urlparse


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(**self.parse_url())
        logging.info("DB connection open")

    @staticmethod
    def parse_url():
        url = urlparse.urlparse(env("DATABASE_URL"))
        return dict(
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
            dbname=url.path[1:],
        )

    async def close(self):
        self.conn.close()
        print("DB connection closed!", flush=True)

    async def change_db(self, command, ids=False):
        cur = self.conn.cursor()
        if ids:
            cur.execute(command, ids)
        else:
            cur.execute(command)
        self.conn.commit()

    async def read_db(self, command, ids):
        F = (False, False, False)
        try:
            cur = self.conn.cursor()
            cur.execute(command, ids)
            q = cur.fetchone()
            return F if not q else q
        except:
            return F

    async def init_table(self):
        await self.change_db(
            "CREATE TABLE IF NOT EXISTS ids(telegram TEXT, discord TEXT, verified BOOL);"
        )
        await self.change_db(
            "CREATE UNIQUE INDEX IF NOT EXISTS id_index ON ids(telegram, discord);"
        )
        logging.info("DB initialized table")

    async def add_chat(self, tg_id, dc_id):
        await self.change_db(
            "INSERT INTO ids(telegram, discord, verified)  VALUES  (%s, %s, false);",
            (str(tg_id), str(dc_id)),
        )

    async def verify_chat(self, dc_id):
        await self.change_db(
            "UPDATE ids SET verified=true WHERE discord=%s;", (str(dc_id),)
        )

    async def fetch_dc_id(self, tg_id):
        return await self.read_db("SELECT * FROM ids WHERE telegram=%s;", (str(tg_id),))

    async def fetch_tg_id(self, dc_id):
        return await self.read_db("SELECT * FROM ids WHERE discord=%s;", (str(dc_id),))
