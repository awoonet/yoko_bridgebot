import time, aiohttp


async def find_ip() -> str:
    async with aiohttp.ClientSession() as client:
        async with client.request("GET", "http://ip-api.com/json/") as response:
            try:
                response.raise_for_status()
                json = await response.json()
                return (
                    f"City:     {json['city']}\n"
                    f"Region:   {json['regionName']}\n"
                    f"Country:  {json['country']} {json['countryCode']}\n"
                    f"IP:       {json['query']}\n\n"
                )
            except:
                return ""


async def turn_on(app):
    bot = app.bot
    json = await find_ip()
    a = (
        "**Turned on bot:** \n\n"
        f"```Bot:      {bot.first_name}\n"
        f"Username: @{bot.username}\n"
        f"User ID:  {bot.id}\n\n"
        f"{json}"
        f"Time:     {time.strftime('%H:%M:%S %d/%m/%Y', time.localtime())}```"
    )

    await app.send_message(app.config_id, a)
