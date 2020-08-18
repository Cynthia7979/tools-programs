import re
from collections import defaultdict
import random
import jieba
import sys,os


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


with open('games.txt', encoding='utf-8') as f:
    gamelist = f.readlines()
with open('wishlist.txt', encoding='utf-8') as f:
    wishlist = f.readlines()

couple_words = defaultdict(LString)
couple_words_cn = defaultdict(LString)


def load(phrases, cn=False):
    with open(phrases, 'r', encoding='utf-8') as f:
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
    words = jieba.cut(message)
    print(words)
    try:
        for i in range(2, len(words)):
            couple_words_cn[(words[i - 2], words[i - 1])].put(words[i])
        couple_words_cn[(words[-2], words[-1])].put("")
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


def generate_cn():
    print(couple_words_cn)
    result = []
    while len(result) < 10 or len(result) > 20:
        result = []
        s = random.choice(list(couple_words_cn.keys()))
        result.extend(s)
        while result[-1]:
            w = couple_words_cn[(result[-2], result[-1])].get_random()
            result.append(w)
    return " ".join(result)


load('chinese_word_sources.txt')
generate()
