from pyrogram	import Client
from funcs.lib	import Chat, check_chat
import discord, os

async def TG_name(u, oth=''):
	if u.username:
		if u.username == 'yoko_bridgebot': return ''
		un = f'{u.username}'
	else: 
		l  = u.last_name if u.last_name	else ''
		un = f'{u.first_name} {l}'

	return f"{oth}**[{un}]**: "

async def spaces(text, ind):
	"""Функция принимает строку, и вставляет перенос строки, 
	если символов 40 или если слово кончается раньше.
	"""
	text_sp = text.split('\n')
	counter = 0
	new_text = ''
	for sentence in text_sp:
		new_text+=f'\n{ind}'
		text = sentence.split()
		for word in text:
			counter += len(word) + 1
			if counter >= 40:
				new_text += f'\n{ind}{word} '
				counter = len(word) + 1
			else:
				new_text += f'{word} '
	return new_text

async def TG_forward_or_reply(msg):
	name = False
	if   msg['forward_from'		  ]: name	= await TG_name(msg['forward_from'])
	elif msg['forward_sender_name']: name	= msg['forward_sender_name']
	elif msg['forward_from_chat'  ]: name 	= msg['forward_from_chat']['title']

	if name: 
		return f'\nForwarded from: {name}'
	elif msg['reply_to_message']:
		r	 = msg['reply_to_message']
		ind = '    **|** '
		name = await TG_name(r['from_user'], ind) 

		text = f"{r['caption'].markdown}\n**MEDIA**" if r['caption'] else r['text'].markdown
		text = await spaces(text, ind)
		return f'\n{name}{text}\n'
	return ''
	
async def text_formatter(msg):
	name 	= await TG_name(msg.from_user)
	first	= await TG_forward_or_reply(msg)
	txt 	= f'{name}{first}'

	if   msg['caption']: txt += msg['caption'].markdown
	elif msg[  'text' ]: txt += msg[  'text' ].markdown

	return txt

class TG(Client):
	@staticmethod
	async def to_discord(app, msg, disc, db):
		q = await check_chat(msg.chat.id, db)
		if q:
			chan = disc.get_channel(q)
			txt  = await text_formatter(msg)
			print(txt)
			z = None
			if msg.media:
				media = await msg.download()
				z = await chan.send(txt, file=discord.File(media))
				os.remove(media)
			if z == None: await chan.send(txt)
		await msg.continue_propagation()

	@staticmethod
	async def list_db(app, disc, msg, db):
		txt=''
		for y in db.values():
			c = str(await y.chat(app, disc))
			print(c)
			txt+=c
		await msg.reply(txt)