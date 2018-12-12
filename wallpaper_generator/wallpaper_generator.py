import os, sys
import log
import pickle
import pygame
import wx
from pygame.locals import *

pygame.init()


@log.logged(fname='WallpaperGenerator')
class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs, size=(1275, 960), title='Wallpaper Generator')


def load():
    f = open('color_sets.wg', 'r')
    return pickle.load(f)


def save():
    f = open('color_sets.wg', 'w')
    pickle.dump(color_sets, f)


def generate(text, rsl, colorst):
    pass


def main():
    global color_sets
    color_sets = load()

