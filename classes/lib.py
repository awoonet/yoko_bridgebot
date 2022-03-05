import time, asyncio, aiohttp


async def find_ip():
    async with aiohttp.ClientSession() as client:
        async with client.request("GET", "http://ip-api.com/json/") as response:
            response.raise_for_status()
            return await response.json()


async def turn_on(app):
    bot = await app.get_me()

    json = await find_ip()
    a = (
        "**Turned on bot:** \n\n"
        f"```Bot:      {bot.first_name}\n"
        f"Username: @{bot.username}\n"
        f"User ID:  {bot.id}\n"
        f"City:     {json['city']}\n"
        f"Region:   {json['regionName']}\n"
        f"Country:  {json['country']} {json['countryCode']}\n"
        f"IP:       {json['query']}\n"
        f"Time:     {time.strftime('%H:%M:%S %d/%m/%Y', time.localtime())}```"
    )

    await app.send_message(app.config_id, a)

    return bot
