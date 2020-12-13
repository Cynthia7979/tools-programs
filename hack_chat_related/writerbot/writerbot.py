import hackchat
import random
import time
import sys, os


class WriteWithMeObject:
    def __init__(self, sender):
        self.sender = sender
        self.last_msg_time = time.time()
        self.records = []
        self.ended = False

    def add_record(self, msg):
        if msg != '[lb]':
            self.records.append(msg)
        else:
            self.records.append('\n')

    def get_results(self):
        print('Getting results for', self.sender, "'s WWMObject")
        return ' '.join(self.records)

    def end_session(self):
        self.ended = True


# Static ones
def get_word_list(file):
    print('Getting word list of', file)
    return [s.strip('\n') for s in open(file).readlines()]


NICKNAME = 'WriterBot'+str(random.randint(1,1000)).zfill(4)
CHAT = hackchat.HackChat(NICKNAME, 'cynthia!')

WWM_MAP = {}  # {sender: WWMObject}
NOUNS = get_word_list('nouns.txt')
VERBS = get_word_list('verbs.txt')
ADJS = get_word_list('adjectives.txt')
REPLIES = ['Got it. Anything more?', 'Sounds good...', 'Great, please continue.']


def handle_message(chat, message, sender):
    print(f'From {sender}: {message}')
    if f'@writerbot' in message.lower():
        if 'write with me' in message.lower():
            write_with_me_init(sender)
    elif sender in WWM_MAP.keys():
        print(sender, 'is an WWM user')
        write_with_me_handle(sender, message)


def handle_join(chat, sender):
    CHAT.send_message(f'@{sender} Welcome to the channel!')
    on_join_channel()


def write_with_me_init(sender):
    print('Initiating WriteWithMe process with', sender)
    WWM_MAP[sender] = WriteWithMeObject(sender)
    CHAT.send_message(f'@{sender} Great! Please type in your first sentence.')
    CHAT.send_message('Add a line break with `[lb]`, get a hint with `[hint]`, and stop at anytime with `[stop]`.')
    CHAT.send_message(f'How about starting with a {random.choice(NOUNS)}?')


def write_with_me_handle(sender, message):
    print(f"Handling {sender}'s new message...")
    if message != '[stop]':
        if message == '[hint]':
            CHAT.send_message(f'What about a {random.choice(ADJS)} {random.choice(NOUNS)}?')
        else:
            WWM_MAP[sender].add_record(message)
            CHAT.send_message('Linebreak added' if message=='[lb]' else random.choice(REPLIES))
    if WWM_MAP[sender].ended:
        if message == '[sv]':
            f = open(f'works/{sender}_{time.time()}')
            f.write(WWM_MAP[sender].get_results())
            f.close()
        del WWM_MAP[sender]
    else:
        CHAT.send_message("That's all? Great! Let's take a look at the result:")
        CHAT.send_message(WWM_MAP[sender].get_results())
        CHAT.send_message('Type `[sv]` to save (to the computer I\'m running on), other things to quit.')


def on_join_channel():
    CHAT.send_message('I am **WriterBot**! `@WriterBot` to use one of the following commands:')
    CHAT.send_message(' `write with me` - practice creative writing with random words/phrases and auto recording.')


print('Running!')
CHAT.on_message += [handle_message]
CHAT.on_join += [handle_join]
on_join_channel()
CHAT.run()
