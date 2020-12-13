import hackchat
import random
import re
import jieba
from string import ascii_lowercase
from collections import defaultdict

# General constants
BOTNAME = 'CynthiaBot_A'


with open('games.txt', encoding='utf-8') as f:
    gamelist = f.readlines()
with open('wishlist.txt', encoding='utf-8') as f:
    wishlist = f.readlines()


# Sentence generation module
CUT_CHARACTERS = True
CN_MAX = 30
CN_MIN = 15
INITIATOR = ('','')  # Syntax candy
END = ''  # Syntax candy
START_FROM_INITIATOR = True


class LString:
    def __init__(self):
        self._total = 0
        self._successors = defaultdict(int)

    def put(self, word):
        self._successors[word] += 1
        self._total += 1

    def get_random(self):
        ran = random.randint(0, self._total - 1)
        for key, value in self._successors.items():
            if ran < value:
                return key
            else:
                ran -= value


couple_words = defaultdict(LString)
couple_words_cn = defaultdict(LString)


def load(phrases, cn=False, encoding='utf-8'):
    with open(phrases, 'r', encoding=encoding) as f:
        for line in f:
            if cn: add_message_cn(line)
            else: add_message(line)


def add_message(message):
    message = re.sub(r'[^\w\s\']', '', message).lower().strip()
    words = message.split()
    try:
        for i in range(2, len(words)):
            couple_words[(words[i - 2], words[i - 1])].put(words[i])
        couple_words[(words[-2], words[-1])].put("")
    except IndexError:
        pass


def add_message_cn(message:str):
    # message = message.re
    if CUT_CHARACTERS:
        buffer = ''
        words = []
        for s in message:
            if s.lower() in ascii_lowercase or s in ascii_lowercase:
                buffer += s
            else:
                if buffer: words.append(buffer)
                buffer = ''
                words.append(s)
        # 作者：鸡贼的鲁鲁修
        # 链接：https://www.zhihu.com/question/357593816/answer/917731790
        # 来源：知乎
        # 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
    else:
        words = list(jieba.cut(message))  # Cut words
    # print(words)
    try:
        couple_words_cn[INITIATOR].put((words[0], words[1]))
        for i in range(2, len(words)):
            couple_words_cn[(words[i - 2], words[i - 1])].put(words[i])
        couple_words_cn[(words[-2], words[-1])].put(END)
    except IndexError:
        pass


def generate():
    result = []
    while len(result) < 10 or len(result) > 20:
        result = []
        s = random.choice(list(couple_words.keys()))
        result.extend(s)
        while result[-1]:
            w = couple_words[(result[-2], result[-1])].get_random()
            result.append(w)
    return " ".join(result)


def generate_cn(from_keywords:tuple=None):
    # print(couple_words_cn)
    result = []
    while len(result) < CN_MIN or len(result) > CN_MAX:
        result = []
        if START_FROM_INITIATOR and not from_keywords:
            s = random.choice(list(couple_words_cn[INITIATOR]._successors.keys()))
        else:
            s = random.choice(list(couple_words_cn.keys())) if not from_keywords else from_keywords
            while s in ('。','，','”','】'):
                s = random.choice(list(couple_words_cn.keys()))
        result.extend(s)
        while result[-1]:
            w = couple_words_cn[(result[-2], result[-1])].get_random()
            result.append(w)
    return "".join(result)


# Network Interactions
def send_file_content(file, chat):
    with open(file, encoding='utf-8') as f:
        content = f.read()
        chat.send_message(content)


def add_chat_source(chat, message, sender):
    if '@CynthiaBot' not in message and '*debug*' not in message and 'CynthiaBot' not in sender:
        with open('./word_sources/chat_log_word_sources.txt', 'a', encoding='utf-8') as f:
            f.write(message+'\n')


def reply(chat, message, sender):
    try:
        if '@CynthiaBot' in message:
            if 'how are you' in message.lower() or 'status' in message.lower():
                with open('status.txt', encoding='utf-8') as f:
                    status = f.read()
                    chat.send_message('Cynthia is currently '+status+'.')

            elif 'say something' in message.lower():
                chat.send_message(f'@{sender} Listen: {generate().capitalize()}.')

            elif '名言警句+' in message:
                try:
                    keywords = tuple(message[message.find('+')+1:].split('|'))
                    if couple_words_cn[keywords]._total != 0:
                        chat.send_message(f'@{sender} 今日名言警句：{generate_cn(keywords)}\n——CynthiaBot')
                    else:
                        chat.send_message(f'@{sender} 无法生成以此组关键词为开头的句子。')
                except IndexError:
                    chat.send_message(f'@{sender} 语法错误。请使用`@CynthiaBot 名言警句+关键词1|关键词2` 生成指定句子（关键词必须为2个）')
            elif '名言警句' in message:
                chat.send_message(f'@{sender} 今日名言警句：{generate_cn()}\n——CynthiaBot')

            elif 'github' in message.lower():
                chat.send_message("Cynthia's GitHub username is [@Cynthia7979](https://github.com/Cynthia7979).")

            elif 'help' in message.lower():
                send_file_content('help.txt', chat)

            elif 'random scp' in message.lower():
                num = random.randint(2, 5999)
                num = str(num).zfill(3)
                chat.send_message(f"Here's a random SCP: [SCP-{num}](http://scp-wiki.net/scp-{num})")
            elif 'random cn scp' in message.lower():
                num = random.randint(2, 2999)
                num = str(num).zfill(3)
                chat.send_message(f"Here's a random CN SCP: [SCP-CN-{num}](http://scp-wiki-cn.wikidot.com/scp-cn-{num})")

            elif 'game' in message.lower():
                chat.send_message(f"**Here's a random game Cynthia has played:** {random.choice(gamelist)}")
                chat.send_message("You'll have to find the shop link by yourself, unfortunately.")
            elif 'wishlist' in message.lower():
                chat.send_message(f"**Here's a random game in Cynthia's wishlist:** {random.choice(wishlist)}")
                chat.send_message("You'll have to find the shop link by yourself, unfortunately.")

            elif 'todo' in message.lower():
                send_file_content('todo.txt', chat)


        if '*debug*' in message.lower():
            if 'couple_words_cn' in message:
                chat.send_message(list(couple_words_cn.keys()))
                print('sent', str(couple_words_cn))
            elif 'couple_words' in message:
                chat.send_message(list(couple_words.keys()))


        if '@Cynthia ' in message and 'Cynthia' not in chat.online_users:
            chat.send_message(f'@{sender} Cynthia is not in the chat right now. Please use `@CynthiaBot how are you`'+
                              f' to check Cynthia\'s status.')
    except Exception as e:
        chat.send_message(f'{e.__class__.__name__}: {e}')


def welcome(chat, nick):
    chat.send_message(f'@{nick}, welcome! Enter `@CynthiaBot help` to view a list of commands.')


def self_on_join(chat):
    chat._send_packet({"cmd": "emote", "text": "*waves*"})
    chat._send_packet({"cmd": "emote",
                       "text": '*says "Hello everyone!! Enter `@CynthiaBot help` to view a list of commands."*'})


if __name__ == "__main__":
    load("./word_sources/SCP_word_sources.txt")
    load('./word_sources/quote_word_sources.txt')
    load('./word_sources/general_en_word_sources.txt')
    load('./word_sources/forum_word_sources.txt')
    load("./word_sources/cn_general_chinese_word_sources.txt", cn=True)
    load('./word_sources/cn_tree_word_sources.txt', cn=True)
    load('./word_sources/cn_chat_log_word_sources.txt', cn=True)
    load('./word_sources/cn_wake-up-in-twilight_word_sources.txt', cn=True)
    # load('./word_sources/cn_sral-9_word_sources.txt', cn=True)
    load('./word_sources/cn_essay_material_word_sources.txt', cn=True, encoding='utf-16-le')
    cynthia_channel = hackchat.HackChat(BOTNAME, 'cynthia!')
    print('Running...')
    self_on_join(cynthia_channel)
    cynthia_channel.on_message += [reply]
    cynthia_channel.on_message += [add_chat_source]
    cynthia_channel.on_join += [welcome]
    cynthia_channel.run()
