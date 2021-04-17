import time, asyncio, aiohttp

async def find_ip():
	async with aiohttp.ClientSession() as client:
		async with client.request('GET', 'http://ipinfo.io/json') as response:
				response.raise_for_status()
				return await response.json()

async def turn_on(app):
	bot = await app.get_me()

	json = await find_ip()
	txt = (f'''**Turned on bot:** ```
User:     {bot.first_name}
Username: @{bot.username}
User ID:  {bot.id}
Time:     {time.strftime("%y/%m/%d %H:%M:%S", time.localtime())}
Location: {json["city"]} ({json["country"]})
IP:       {json["ip"]}```''')

	await app.send_message(app.config_id, txt)

	return bot

