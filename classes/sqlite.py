import sqlite3

class Database:
	def __init__(self, adress):
		self.adress = adress
		self.conn 	= sqlite3.connect(self.adress)

	async def close(self):
		self.conn.close()
		print('DB connection closed!', flush=True)	

	async def change_db(self, command, ids=False):
		cur = self.conn.cursor()
		if ids:	cur.execute(command, ids)
		else:		cur.execute(command)
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
		await self.change_db("CREATE TABLE IF NOT EXISTS ids(telegram INTEGER, discord INTEGER, verified INTEGER);")

	async def add_chat(self, tg_id, dc_id):
		await self.change_db("INSERT INTO ids(telegram, discord, verified)  VALUES  (?, ?, 0)", (tg_id, dc_id))
	
	async def verify_chat(self, dc_id):
		await self.change_db("UPDATE ids SET verified=1 WHERE discord=?", (dc_id,))

	async def fetch_dc_id(self, tg_id):
		return await self.read_db("SELECT * FROM ids WHERE telegram=?", (tg_id,))

	async def fetch_tg_id(self, dc_id):
		return await self.read_db("SELECT * FROM ids WHERE discord=?", (dc_id,))
		