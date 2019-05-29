# https://www.codingame.com/playgrounds/41655/how-to-build-a-chatbot-in-less-than-50-lines-of-code
# -*- coding: utf-8 -*-
import random, re
from collections import defaultdict

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

def load(phrases):
    with open(phrases, 'r') as f:
        for line in f:
            add_message(line)

def add_message(message):
    message = re.sub(r'[^\w\s\']', '', message).lower().strip()
    words = message.split()
    try:
        for i in range(2, len(words)):
            couple_words[(words[i - 2], words[i - 1])].put(words[i])
        couple_words[(words[-2], words[-1])].put("")
    except IndexError:
        pass

def generate():
    result = []
    while len(result) < 10 or len(result) > 40:
        result = []
        s = random.choice(list(couple_words.keys()))
        result.extend(s)
        while result[-1]:
            w = couple_words[(result[-2], result[-1])].get_random()
            result.append(w)

    return " ".join(result)

if __name__ == "__main__":
    load("chatbot/scp.txt")
    print(generate())
