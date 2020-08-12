import hackchat
import re
import random


def try_reply(chat, message, sender):
    print(f'{message} ~{sender}')
    if message == '/help':
        chat.send_message('Unknown command. Type "/help" for help.')
    if message.lower() == '@helpbot mod me' and '@HelpBot' in message:
        chat._send_packet({'cmd': 'addmod', 'trip': sender})
        chat.send_message('Modded.')
    if re.search('[0-9]+d[0-9]+', message):
        print('matched')
        xdx = re.search('[0-9]+d[0-9]+', message).group(0)
        multiply = int(xdx[:xdx.find('d')])
        dice_range = int(xdx[xdx.find('d')+1:])
        chat.send_message(f'{xdx} = {multiply*random.randint(0,dice_range)}')


def welcome(chat, user):
    chat.send_message(f'{user}, welcome to the chat!!!')

main_chat = hackchat.HackChat('HelpBot', 'cynthia!')
# test()
main_chat.on_message += [try_reply]
main_chat.on_join += [welcome]
main_chat.run()
