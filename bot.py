import telepot
import urllib.request
import json
import threading

TOKEN = '538084148:AAFT90I8FHMZ0df3ZYtZIF5vspbGR5Ar3mA'
kick = False
priv = False
boolean = False
settings = {
	'antibot':True,
	'messages_per_second':3
}
antiflood = {}

def newgroup(msg):
	if msg['chat']['type'] == "supergroup":
		chatid = msg['chat']['id']
		groupfile = open('groups.txt').read()
		if str(chatid) in groupfile:
			boolean = False
		else:
			group = open("groups.txt", "a")
			group.write(str(chatid) + "\n")
			print("[i] the bot has been added to a new group(" + str(chatid) + ")")
			boolean = True

def addblacklist(msg):
	text = msg['text']
	chatid = msg['chat']['id']
	if text.startswith('/addblacklist'):
		iddi = text.split(' ')[1]
		blacklist = open("blacklist.txt", "a")
		blacklist.write(iddi + "\n", )
		bot.sendMessage(chatid, iddi + " blacklisted")

def blacklist(msg):
	blacklist = open("blacklist.txt").read()
	chatid = msg['chat']['id']
	user = msg['from']['id']
	name = msg['from']['first_name']
	if str(user) in blacklist:
		bot.kickChatMember(chatid, user)
		bot.sendMessage(chatid, name + " is on *blacklist*", parse_mode='Markdown')


def antibot(msg):
	information = bot.getChatMember(msg['chat']['id'], msg['from']['id'])
	if 'new_chat_members' in msg:
		msgid = msg['message_id']
		chat = msg['chat']['id']
		new = msg['new_chat_members']
		for x in new:
			if information['status'] == "member":
				if x['is_bot'] == True:
					chat = msg['chat']['id']
					bot.kickChatMember(chat, msg['from']['id'])
					bot.kickChatMember(chat, x['id'])
					print("[i] " + str(chat) + " -> banned bot " + str(x['id']))
					kick = True
			else:
				kick = False

def on_chat_message(msg):
	if msg['chat']['type'] == "supergroup":
		content_type, chat_type, chat_id = telepot.glance(msg)
		try:
			print(msg['from']['first_name'] + "(" + str(msg['from']['id']) + ") -> " + msg['chat']['title'] + "(" + str(msg['chat']['id']) + ") -> " + msg['text'])
			priv = True
		except KeyError:
			priv = False
		if content_type == 'text':
			name = msg["from"]["first_name"]
			txt = msg['text']
			chat_id = msg['chat']['id']
			user_id = msg['from']['id']
			info = bot.getChatMember(chat_id, user_id)
			if txt.startswith('/start'):
				bot.sendMessage(chat_id, 'Hey *' + msg['from']['first_name'] + "*! I am working", parse_mode='Markdown')
			if txt.startswith('/help'):
				bot.sendMessage(chat_id, '<b>Commands List</b>:\n - /start\n - /help\n - /ban (reply)\n - /unban (reply)\n\n<code>[+]</code> <b>This bot contain AntiFlood</b>\n<code>[+]</code> <b>This bot contain AntiBot</b>\n<code>[+]</code> <b>This bot contain a BlackList against spammer</b>', parse_mode='html')
			if txt.startswith('/ban'):
				if info['status'] == "administrator" or "creator":
					bot.kickChatMember(chat_id, msg['reply_to_message']['from']['id'])
					bot.sendMessage(chat_id, msg['reply_to_message']['from']['first_name'] + " has been *banned*.", parse_mode='Markdown')
					boolean = True
				elif info['status'] == "member":
					boolean = False
			if txt.startswith('/unban'):
				if info['status'] == "administrator" or "creator":
					bot.unbanChatMember(chat_id, msg['reply_to_message']['from']['id'])
					bot.sendMessage(chat_id, msg['reply_to_message']['from']['first_name'] + " has been *unbanned*.", parse_mode='Markdown')
					boolean = True
				elif info['status'] == "member":
					boolean = False
	elif msg['chat']['type'] == "private":
		chat_id = msg['chat']['id']
		if msg['text'].startswith('/start'):
			bot.sendMessage(chat_id, "Hey ! Add me to a group, give me admin permissions, and I will protect it.💀\nPress /help to know what commands you can do.\n\n<a href='https://telegram.me/xxhammerbot?startgroup=test'>Click here for add me in a group</a>", parse_mode='html')
		if msg['text'].startswith('/help'):
			bot.sendMessage(chat_id, '<b>Commands List</b>:\n - /start\n - /help\n - /ban (reply)\n - /unban (reply)\n\n<code>[+]</code> <b>This bot contain AntiFlood</b>\n<code>[+]</code> <b>This bot contain AntiBot</b>\n<code>[+]</code> <b>This bot contain a BlackList against spammer</b>', parse_mode='html')


def general(msg):
    t1 = threading.Thread(target=antibot, args=(msg,),)
    t1.start()

    t2 = threading.Thread(target=on_chat_message, args=(msg,),)
    t2.start()

    t4 = threading.Thread(target=blacklist, args=(msg,),)
    t4.start()

    t5 = threading.Thread(target=addblacklist, args=(msg,),)
    t5.start()

    t6 = threading.Thread(target=newgroup, args=(msg,),)
    t6.start()

if __name__ == '__main__':
    bot = telepot.Bot(TOKEN)
    bot.message_loop(general)

    print('Caricando...')

    import time
    while 1:
        time.sleep(10)
