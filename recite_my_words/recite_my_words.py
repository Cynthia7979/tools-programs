import pygame
import sys, os
import requests
import random
import tkinter as tk
from pygame.locals import *


def download_voice(word):
    url = f'http://dict.youdao.com/dictvoice?audio={word}&type={random.randint(1, 2)}'
    r = requests.get(url)
    with open('dictvoice.mp3', 'wb') as f:
        f.write(r.content)
        return f


def main():
    pygame.init()
    pygame.mixer.init()
    WINDOW = pygame.display.set_mode((960, 640))
    words = []
    with open('write_your_words_here.txt') as f:
        lns = f.readlines()
        for l in lns:
            if not l.startswith('#'):
                words.append(l.strip('\n'))
    current_word = 0
    rarrow = pygame.image.load('rightarrow.png')
    arr_rect = rarrow.get_rect()
    arr_rect.midbottom = (960/2, 640*0.75)
    font = pygame.font.Font()
    while True:
        WINDOW.blit(rarrow, arr_rect)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
