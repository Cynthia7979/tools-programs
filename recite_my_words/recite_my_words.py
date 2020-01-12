import pygame
import sys, os
import requests
import random
from bs4 import BeautifulSoup as bsoup
from pygame.locals import *
from tkinter.filedialog import askopenfilename, Tk


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
    if not os.path.exists(f'{word}_1.mp3') or not os.path.exists(f'{word}_2.mp3'):
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
    try:
        translations = result_box.find_all('li')
    except AttributeError:
        return '无法获取释义'
    results = []
    for t in translations:
        results.append(t.get_text())
    return '；'.join(results)


def main():
    pygame.init()
    pygame.mixer.init()
    WINDOW = pygame.display.set_mode(SIZE)
    words = []
    not_recited_words = []
    all_not_recited_words = {}
    current_word = 0
    finished = False
    played = False
    display_chinese = False
    chi_trans = None

    root = Tk()
    word_list = askopenfilename(filetypes=(('Text File', '.txt'),))
    root.destroy()
    word_list = word_list if word_list else 'write_your_words_here.txt'
    with open(word_list) as f:
        lns = f.readlines()
        for l in lns:
            if not l.startswith('#'):
                w = l.strip('\n')
                w = w[:w.find('(')-1] if '(' in w else w
                words.append(w)
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

    wrong = pygame.image.load('wrong.png')
    wrong = pygame.transform.scale(wrong, (int(HEIGHT/8),)*2)
    wrong_rect = wrong.get_rect()
    wrong_rect.midright = (arr_rect.left-30, arr_rect.centery)

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
            WINDOW.blit(wrong, wrong_rect)
            # Displaying the Eng word
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
                with open(f'{os.path.dirname(word_list)}/review-'
                          f'{os.path.basename(word_list)}.txt', 'w') as review_file:
                    # for w, fq in all_not_recited_words.items():
                    review_file.write('\n'.join([f'{w} (x{fq})' for w, fq in all_not_recited_words.items()]))
                    # E.g. tree (x10)\n
                    # apple(x1)\n
                    # sweet(x2)
                delmp3s()
                pygame.quit()
                sys.exit()
            elif e.type == MOUSEBUTTONUP:
                pos = e.pos
                next_word = False
                if playrect.collidepoint(pos):
                    play_sound(words[current_word])
                elif chi_rect.collidepoint(pos):
                    display_chinese = True
                elif wrong_rect.collidepoint(pos):
                    w = words[current_word]
                    not_recited_words.append(w)
                    if w not in list(all_not_recited_words.keys()):
                        all_not_recited_words[w] = 1
                    else:
                        all_not_recited_words[w] += 1
                    next_word = True
                if arr_rect.collidepoint(pos) or next_word:
                    current_word += 1
                    if current_word >= len(words) and not_recited_words == []:
                        finished = True
                        delmp3s()
                    elif current_word >= len(words) and not_recited_words != []:
                        current_word = 0
                        words, not_recited_words = not_recited_words, []
                        played = False
                        chi_trans = None
                        display_chinese = False
                    else:
                        played = False
                        chi_trans = None
                        display_chinese = False
        pygame.display.flip()
        CLOCK.tick(FPS)




if __name__ == '__main__':
    main()
