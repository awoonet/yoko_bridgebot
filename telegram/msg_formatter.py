async def fetch_text(msg):
	"""Возвращает caption, text или ничего из сообщения"""
	if 		msg.text 		is not None:	return msg.text.markdown.replace('__', '_')
	elif  msg.caption is not None:	return msg.caption.markdown.replace('__', '_')
	else:														return ''

async def fetch_name(user):
	"""Возвращает username, имя с фамилией или просто имя 
	отформатированное в соответствии с полученной командой."""
	if user.username is not None:
		un = f"@{user.username}" 
	elif user.last_name is not None:
		un = f"{user.first_name} {user._last.name}"
	else:
		un = user.first_name		
	return f"**[{un}]**: "

async def forwarded(msg):
	answer = ''
	if msg.forward_from is not None: 
		answer = f'от пользователя:** *{await fetch_name(msg.forward_from)}'
	elif msg.forward_sender_name is not None: 
		answer = f'от пользователя:** *{msg.forward_sender_name}'
	elif msg.forward_from_chat is not None: 
		answer = f'из канала:** *{msg.forward_from_chat.title}'
	return f'\n**Переслано {answer}*\n' if answer else ''

async def format_msg(msg):
	name = await fetch_name(msg.from_user)
	text = await fetch_text(msg)
	fwd  = await forwarded(msg)
	return f'{name}{fwd}{text}'

async def spaces(text, ind='   **|** '):
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

			if counter >= 70:
				new_text += f'\n{ind}{word} '
				counter = len(word) + 1

			else:
				new_text += f'{word} '

	return new_text

async def reply_msg(msg):
	if msg.reply_to_message is not None: 
		text = await format_msg(msg.reply_to_message)
		#text = await spaces(text)
		q = '-'*40
		return (f"В ответ на сообщение:\n{q}\n{text}\n{q}\n")
	return ''

async def text_formatter(self, msg):
	rpl = await reply_msg(msg)
	msg = await format_msg(msg)
	return f'{rpl}{msg}'


