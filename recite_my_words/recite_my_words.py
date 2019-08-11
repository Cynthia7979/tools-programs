import pygame
import sys, os
import requests
import random
import tkinter as tk
from bs4 import BeautifulSoup as bsoup
from pygame.locals import *


WHITE = (255,255,255)
BLACK = (0  ,0  ,0  )
WIDTH, HEIGHT = SIZE = (960, 640)
CLOCK = pygame.time.Clock()
FPS = 30


def download_voice(word):
    url1 = f'http://dict.youdao.com/dictvoice?audio={word}&type=1'
    url2 = f'http://dict.youdao.com/dictvoice?audio={word}&type=2'
    r1 = requests.get(url1)
    r2 = requests.get(url2)
    with open(f'{word}_1.mp3', 'wb') as f:
        f.write(r1.content)
    with open(f'{word}_2.mp3', 'wb') as f:
        f.write(r2.content)


def play_sound(word):
    if not os.path.exists(f'{word}_1.mp3'):
        download_voice(word)
    pygame.mixer.music.load(f'{word}_{random.randint(1,2)}.mp3')
    pygame.mixer.music.play()


def delmp3s():
    mp3s = []
    for rt, dirs, files in os.walk('.'):
        for filename in files:
            if filename.endswith('mp3'):
                mp3s.append(filename)
    for mp in mp3s:
        try:
            os.remove(mp)
        except PermissionError:
            pass


def get_chinese(word):
    url = f'http://dict.youdao.com/w/eng/{word}'
    html = requests.get(url).content
    soup = bsoup(html, 'html.parser', from_encoding='utf-8')
    result_box = soup.find('div', id='phrsListTab')
    translations = result_box.find_all('li')
    results = []
    for t in translations:
        results.append(t.get_text())
    return '；'.join(results)


def main():
    pygame.init()
    pygame.mixer.init()
    WINDOW = pygame.display.set_mode(SIZE)
    words = []
    with open('write_your_words_here.txt') as f:
        lns = f.readlines()
        for l in lns:
            if not l.startswith('#'):
                words.append(l.strip('\n'))
    current_word = 0
    finished = False
    played = False
    display_chinese = False
    chi_trans = None
    rarrow = pygame.image.load('rightarrow.png')
    rarrow = pygame.transform.scale(rarrow, (int(HEIGHT/3),)*2)
    arr_rect = rarrow.get_rect()
    arr_rect.midbottom = (WIDTH/2, HEIGHT*0.75)
    congrats = pygame.image.load('congratulations.jpg')
    congrats = pygame.transform.scale(congrats, SIZE)
    cong_rect = congrats.get_rect()
    cong_rect.topleft = (0, 0)
    play = pygame.image.load('play-button.png')
    play = pygame.transform.scale(play, (int(HEIGHT/10),)*2)
    playrect = play.get_rect()
    playrect.topleft = (WIDTH*0.75, HEIGHT*0.25)
    chinese = pygame.image.load('chinese.png')
    chinese = pygame.transform.scale(chinese, (int(HEIGHT/10),)*2)
    chi_rect = chinese.get_rect()
    chi_rect.midleft = playrect.midright
    font = pygame.font.Font('ZCOOLXiaoWei-Regular.ttf', 36)
    small_font = pygame.font.Font('ZCOOLXiaoWei-Regular.ttf', 20)
    while True:
        WINDOW.fill(WHITE)
        if finished:
            WINDOW.blit(congrats, cong_rect)
        else:
            WINDOW.blit(rarrow, arr_rect)
            WINDOW.blit(play, playrect)
            WINDOW.blit(chinese, chi_rect)
            word_surf = font.render(words[current_word], True, BLACK)
            word_rect = word_surf.get_rect()
            word_rect.midtop = (WIDTH/2, HEIGHT*0.25)
            WINDOW.blit(word_surf, word_rect)
            if not played:
                play_sound(words[current_word])
                played = True
            if display_chinese:
                if not chi_trans:
                    chi_trans = get_chinese(words[current_word])
                trans_surf = small_font.render(chi_trans, True, BLACK)
                trans_rect = trans_surf.get_rect()
                trans_rect.midbottom = word_rect.midtop
                WINDOW.blit(trans_surf, trans_rect)
        for e in pygame.event.get():
            if e.type == QUIT:
                delmp3s()
                pygame.quit()
                sys.exit()
            elif e.type == MOUSEBUTTONUP:
                pos = e.pos
                if arr_rect.collidepoint(pos):
                    current_word += 1
                    if current_word == len(words):
                        finished = True
                    else:
                        played = False
                        chi_trans = None
                        display_chinese = False
                        delmp3s()
                elif playrect.collidepoint(pos):
                    play_sound(words[current_word])
                elif chi_rect.collidepoint(pos):
                    display_chinese = True

        pygame.display.flip()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()