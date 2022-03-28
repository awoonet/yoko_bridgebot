import logging, discord

from disc.helpers import Helpers

w = logging.warning


class Discord(discord.Client, Helpers):
    katsu_id = 435531611543437312

    async def on_ready(self):
        logging.warning(f" Discord bot started as {self.user}")

    async def on_message(self, msg):
        if msg.author == self.user:
            return

        tg_id, _, verified = await self.db.fetch_tg_id(msg.channel.id)

        try:
            if "/embed" in msg.content:
                await self.send_embed(msg)

            elif verified:
                txt = f"**{msg.author.name}:** {msg.content}"

                if msg.content:
                    await self.tg.send_message(chat_id=tg_id, text=txt)
                else:
                    media_url = msg.attachments[0].url
                    await self.send_media(tg_id, media_url, txt)

            elif tg_id:
                await self.add_bridge(self, self.db, msg)
        except Exception as e:
            await self.tg.send_error_msg(msg, e)
