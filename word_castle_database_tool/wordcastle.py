import argparse
import sys, os
import sqlite3
import xml.etree.ElementTree as ET

DEBUG_ARGS = '--youdao test.xml'.split()
COLUMNS = """(
                wordId INT PRIMARY KEY, 
                spell TEXT,
                phoneticSymbol TEXT,
                explaination TEXT,
                sentenceEN TEXT,
                sentenceCH TEXT,
                pronouncationURL TEXT,
                wordLength INT,
                learnedTimes INT DEFAULT 0,
                ungraspTimes INT DEFAULT 0,
                isFamiliar INT DEFAULT 0,
                backupPronounciationURL TEXT
             )"""

def main():
    parser = argparse.ArgumentParser(
        description='Generate word castle .db files with YouDao XML or custom words.'
    )
    parser.add_argument(
        '-t', '--txt',
        action='store',
        dest='txt_path',
        metavar='path',
        help='Path of txt file',
        type=str
    )
    parser.add_argument(
        '-y', '--youdao',
        action='store',
        dest='yd_path',
        metavar='path',
        help='Path of YouDao wordbook file. This overwrites the txt file.',
        type=str
    )
    parser.add_argument(
        '-o', '--output',
        action='store',
        default='output.db',
        dest='output',
        help='Path of output db file. Defaults to "output.db".',
        type=str
    )
    parser.add_argument(
        '-w', '--add-word',
        action='store',
        nargs='+',
        dest='words',
        help='Adds words to an existing .db file',
        type=list
    )
    parser.add_argument(
        '-i', '--init',
        action='store',
        dest='init_file',
        metavar='filename',
        help='Creates an empty .db file in Word Castle format.',
        type=str
    )

    if len(sys.argv) == 1:  # Debug
        print('WARNING: You did not pass any arguments. This will parse', DEBUG_ARGS)
        args = parser.parse_args(DEBUG_ARGS)
    else:
        args = parser.parse_args()

    assert args.output.endswith('.db'), 'Output file must be .db file.'
    assert args.yd_path or args.txt_path or args.words or args.init_file,\
        'You must use one of these switches: -y, -t, -w, -i'

    if args.yd_path:
        assert args.yd_path.endswith('.xml'), 'YouDao file must be in XML format.'
        xml2db(args.yd_path)
    elif args.txt_path:
        assert args.yd_path.endswith('.xml'), 'TXT file must be in TXT format.'
        # txt2db(args.txt_path)
    elif args.words:
        pass
    elif args.init_file:
        db_init(args.init_file)


def xml2db(path):
    xmlf = ET.parse(path)
    root = xmlf.getroot()
    for item in root:
        print(str(item))


def db_init(path):
    """
    Creates a new .db file in Word Castle format.
    :param path: Path of .db file
    :return: (Connection, Cursor)
    """
    if os.path.exists(path):
        if input(f'WARNING: DB file {path} already exists. Proceed? (y/n)').lower == 'n':
            sys.exit()
        else:
            print('Overwriting', path)
    open(path, 'w').close()  # touch
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('CREATE TABLE SIMPLE '+COLUMNS)
    cur.execute('CREATE TABLE MEDIUM '+COLUMNS)
    cur.execute('CREATE TABLE MASTER '+COLUMNS)
    return conn, cur


def db_load(path):
    """
    Loads an existing .db file
    :param path: Path of .db file
    :return: (Connection, Cursor)
    """
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    return conn, cur


if __name__ == '__main__':
    main()
