from distutils.core import setup
import py2exe

setup(windows = [{"script":'click.py'}], options={"py2exe":{"includes":["Tkinter"]}})
