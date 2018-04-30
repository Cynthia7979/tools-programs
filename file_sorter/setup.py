from distutils.core import setup
import py2exe

setup(windows = [{"script":'file_sorter.py'}], options={"py2exe":{"includes":["Tkinter", "shutil", "os"]}})