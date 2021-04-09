import argparse
import sqlite3
import xml.etree.ElementTree as ET

arg_parser = argparse.ArgumentParser(
    usage='Generate word castle .db files with YouDao XML or custom words'
)
arg_parser.add_argument(
    '--txt',
    action='store',
    help='Path of txt file'
)
arg_parser.add_argument(
    '--youdao',
    action='store',
    help='Path of YouDao wordbook file. This overwrites the txt file.'
)



