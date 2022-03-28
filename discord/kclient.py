import logging
import mimetypes

import discord

w = logging.warning


class Discord(discord.Client):
    katsu_id = 435531611543437312

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
            print(e, flush=True)

    async def send_media(self, chat_id, url, txt):
        app = self.tg
        media_type = (mimetypes.guess_type(url=url))[0]

        vars = dict(chat_id=chat_id, caption=txt)

        if "gif" in media_type:
            await app.send_animation(animation=url, **vars)
        elif "image" in media_type:
            await app.send_photo(photo=url, **vars)
        elif "audio" in media_type:
            await app.send_audio(audio=url, **vars)
        elif "video" in media_type:
            await app.send_video(video=url, **vars)
        else:
            await app.send_document(document=url, **vars)

    async def add_bridge(self, _, db, msg):
        conditions = (
            (
                await self.check_admin(msg),
                "Тебе нужно быть администратором, чтобы подтвердить установку моста.",
            ),
            (
                "verify_bridge" in msg.content,
                "Подтвердите, пожалуйста, установку моста, написав: verify_bridge",
            ),
        )

        condition = True
        for i in conditions:
            if not i[0]:
                condition = i[0]
                answer = i[1]

        if condition:
            await db.verify_chat(msg.channel.id)
            answer = "Подтверждено, мост проложен."

        await self.send_message(msg.channel.id, answer)

    async def send_message(self, chat_id: int, txt: str, file=None):
        if file is not None:
            file = discord.File(fp=file)
        else:
            await self.get_channel(chat_id).send(content=txt, file=file)

    async def check_admin(self, msg):
        is_admin = msg.author.guild_permissions.administrator
        is_katsu = msg.author.id == self.katsu_id
        return is_admin or is_katsu

    @staticmethod
    async def send_embed(msg):
        embed = discord.Embed()
        embed.description = (msg.content).replace("/embed ", "")
        await msg.reply(embed=embed)
