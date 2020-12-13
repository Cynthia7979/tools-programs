import hackchat
import random
import os
from datetime import date


# Local
def get_word_list(file):
    print('Getting word list of', file)
    return [s.strip('\n') for s in open(file).readlines()]


def save_work(filename, author, content):
    print('Saving', filename, 'by', author)
    path = f'works/{filename}_{author}.txt'
    with open(path, 'w') as f:
        f.write(content)
    return path


# Global Variables
NICKNAME = 'WriterBot'+str(random.randint(1,1000)).zfill(4)
CHAT = hackchat.HackChat(NICKNAME, 'cynthia!')
INTRO = """I am **WriterBot**! `@WriterBot` to use one of the following commands:
* `writewithme` - practice creative writing with random words/phrases and auto recording.
* `flashfiction` - get a quick idea for writing a story with less than 50 words.
* `save <filename> <content>` - save a specific work to my computer
* `browse` - browse works written by others
* `read <filename>` - read a specific work"""


# Actions
def handle_message(chat, message:str, sender):
    print(f'From {sender}: {message}')
    args = message.split()
    if args[0] == '@writerbot' and len(args) > 1:
        command = args[1].lower()
        if command == 'writewithme':
            write_with_me_init(sender)
        elif command == 'flashfiction':
            flash_fiction(sender)
        elif command == 'save':
            custom_save(sender, args)
        elif command == 'browse':
            browse()
        elif command == 'read':
            read(args)
    elif sender in WWM_MAP.keys():
        print(sender, 'is an WWM user')
        write_with_me_handle(sender, message)


def handle_join(chat, sender):
    CHAT.send_message(f'@{sender} Welcome to the channel!')
    CHAT.send_message(INTRO)


def on_join_channel():
    CHAT.send_message(INTRO)


# misc functions
def flash_fiction(sender):
    CHAT.send_message(f"@{sender} Okay... Write a Flash Fiction (<50 words) with a **{random.choice(NOUNS)}** " +
                      f"and a **{random.choice(ADJS)} {random.choice(NOUNS)}**.")
    CHAT.send_message('After you finish, you can use `@writerbot save <filename>` to save your work!')


def custom_save(sender, args):
    try:
        filename = args[2]
        content = ' '.join(args[3:])
        save_work(filename, sender, content)
        CHAT.send_message(f'@{sender} Your work have been saved.')
    except IndexError:
        CHAT.send_message(f'@{sender} Please check your syntax, the correct one should be `save <filename>`!')


def browse():
    list_of_works = []
    for _, _, files in os.walk('works/'):
        list_of_works = ['* '+fn.strip('.txt') for fn in files]
    if list_of_works:
        CHAT.send_message('Here is a list of works available:\n'+'\n'.join(list_of_works))
    else:
        CHAT.send_message("There's no works available now. Come again later!")


def read(args):
    try:
        filename = args[2]
        with open(f'works/{filename}.txt') as f:
            CHAT.send_message(f.read())
    except IndexError:
        CHAT.send_message('Please specify a filename with `@writerbot read <filename>`!')
    except FileNotFoundError:
        CHAT.send_message(f"There's no {filename} present. Please check your spelling.")


# Write With Me
class WriteWithMeObject:
    def __init__(self, sender):
        self.sender = sender
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


WWM_MAP = {}  # {sender: WWMObject}
NOUNS = get_word_list('nouns.txt')
VERBS = get_word_list('verbs.txt')
ADJS = get_word_list('adjectives.txt')
REPLIES = ['Got it. Anything more?', 'Sounds good...', 'Great, please continue.']


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
            CHAT.send_message(f'@{sender} What about a {random.choice(ADJS)} {random.choice(NOUNS)}?')
        else:
            WWM_MAP[sender].add_record(message)
            CHAT.send_message(f'@{sender} Linebreak added' if message=='[lb]'
                              else f'@{sender} {random.choice(REPLIES)}')
    if WWM_MAP[sender].ended:
        if message == '[sv]':
            path = save_work('WWM_'+date.today().strftime('%H%M%S'),
                             sender,
                             WWM_MAP[sender].get_results())
            CHAT.send_message(f'Saved to {path}')
        del WWM_MAP[sender]
        print('WriteWithMe session with', sender, 'ended')
    else:
        CHAT.send_message("That's all? Great! Let's take a look at the result:")
        CHAT.send_message(WWM_MAP[sender].get_results())
        CHAT.send_message('Type `[sv]` to save (to the computer I\'m running on), other things to quit.')


# Main
print('Running!')
CHAT.on_message += [handle_message]
CHAT.on_join += [handle_join]
on_join_channel()
CHAT.run()
