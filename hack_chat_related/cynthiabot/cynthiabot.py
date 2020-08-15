import hackchat
import random


with open('games.txt', encoding='utf-8') as f:
    gamelist = f.readlines()
with open('wishlist.txt', encoding='utf-8') as f:
    wishlist = f.readlines()


def reply(chat, message, sender):
    if '@CynthiaBot' in message:
        if 'how are you' in message.lower():
            with open('status.txt', encoding='utf-8') as f:
                status = f.read()
                chat.send_message('Cynthia is currently '+status.lower()+'.')

        elif 'github' in message.lower():
            chat.send_message("Cynthia's GitHub username is [@Cynthia7979](https://github.com/Cynthia7979).")

        elif 'help' in message.lower():
            with open('help.txt', encoding='utf-8') as f:
                help_doc = f.read()
                chat.send_message(help_doc)

        elif 'random scp' in message.lower():
            num = random.randint(2, 5999)
            num = str(num).zfill(3)
            chat.send_message(f"Here's a random SCP: [SCP-{num}](http://scp-wiki.net/scp-{num})")
        elif 'random cn scp' in message.lower():
            num = random.randint(2, 2999)
            num = str(num).zfill(3)
            chat.send_message(f"Here's a random SCP: [SCP-CN-{num}](http://scp-wiki-cn.wikidot.com/scp-cn-{num})")

        elif 'game' in message.lower():
            chat.send_message(f"**Here's a random game Cynthia has played:** {random.choice(gamelist)}")
            chat.send_message("You'll have to find the shop link by yourself, unfortunately.")
        elif 'wishlist' in message.lower():
            chat.send_message(f"**Here's a random game in Cynthia's wishlist:** {random.choice(wishlist)}")
            chat.send_message("You'll have to find the shop link by yourself, unfortunately.")

    if '@Cynthia' in message and 'Cynthia' not in chat.online_users:
        chat.send_message(f'@{sender} Cynthia is not in the chat right now.')


def welcome(chat, nick):
    chat.send_message(f'@{nick}, welcome! Type `@CynthiaBot help` to view a list of commands.')


cynthia_channel = hackchat.HackChat('CynthiaBot', 'cynthia!')
cynthia_channel.on_message += [reply]
cynthia_channel.on_join += [welcome]
cynthia_channel.run()
