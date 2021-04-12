import argparse
import sys, os
import sqlite3
import xml.etree.ElementTree as ET

DEBUG_ARGS = '--youdao test.xml'.split()

COLUMNS = """(
                wordId int IDENTITY(0,1) PRIMARY KEY, 
                spell text,
                phoneticSymbol text DEFAULT '[]',
                explaination text DEFAULT '[]',
                sentenceEN text DEFAULT '',
                sentenceCH text DEFAULT '',
                pronouncationURL text DEFAULT '',
                wordLength text DEFAULT '',
                learnedTimes int DEFAULT 0,
                ungraspTimes int DEFAULT 0,
                isFamiliar int DEFAULT 0,
                backupPronounciationURL text DEFAULT ''
             );"""

VOICE_URL_1 = "http://dict.youdao.com/dictvoice?audio={word}&type=1"
VOICE_URL_2 = "http://dict.youdao.com/dictvoice?audio={word}&type=2"


def main():
    parser = parser_init()

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
        conn, cur = xml2db(args.yd_path, *db_init(args.output))
        conn.close()
    elif args.txt_path:
        assert args.yd_path.endswith('.xml'), 'TXT file must be in TXT format.'
        # txt2db(args.txt_path, *db_init(args.output))
    elif args.words:
        pass
    elif args.init_file:
        db_init(args.init_file)


def xml2db(path, conn:sqlite3.Connection, cur: sqlite3.Cursor):
    xmlf = ET.parse(path)
    root = xmlf.getroot()

    for item in root:
        item_values = {}
        for child in item:
            print(child)
            if child.tag == 'word':
                item_values['spell'] = child.text
            elif child.tag == 'trans':
                text = child.text.replace('\n', '').replace('adj.', '<color=orange>adj.</color>').\
                    replace('n.', '<color=orange>n.</color> ').replace('v.', '<color=orange>v.</color> ').\
                    replace('adv.', '<color=orange>adv.</color> ').replace('int.', '<color=orange>int.</color> ')
                item_values['explaination'] = text
            elif child.tag == 'phonetic':
                item_values['phoneticSymbol'] = child.text
        if not cur.execute('SELECT * from SIMPLE').fetchall():
            next_id = 0
        else:
            next_id = cur.lastrowid
        cur.execute(f"""
            INSERT INTO SIMPLE (
                wordId, spell, phoneticSymbol, explaination, pronouncationURL, wordLength, backupPronounciationURL
            ) VALUES (
                '{next_id}', '{item_values["spell"]}', '{item_values["phoneticSymbol"]}', '[{item_values["explaination"]}]', 
                '{VOICE_URL_1.format(word=item_values['spell'])}', '{len(item_values['spell'])}', 
                '{VOICE_URL_2.format(word=item_values['spell'])}'
            );""")
    conn.commit()
    return conn, cur


def parser_init():
    parser = argparse.ArgumentParser(
        description='Generate word castle .db files with YouDao XML or custom words.',

    )
    parser.add_argument(
        '-t', '--txt',
        action='store',
        dest='txt_path',
        metavar='PATH',
        help='Converts specified TXT file into WordCastle DB.',
        type=str
    )
    parser.add_argument(
        '-y', '--youdao', '--xml',
        action='store',
        dest='yd_path',
        metavar='PATH',
        help='Converts specified YouDao XML file into WordCastle DB. This overwrites the txt file.',
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
        help='Adds words to SIMPLE table of an existing .db file (specified with --db).',
        type=list
    )

    parser.add_argument(
        '--db', '--database',
        action='store',
        dest='exist_db',
        metavar='FILENAME',
        help='Path to the existing database. Create one with -i.',
        type=str
    )
    parser.add_argument(
        '-i', '--init',
        action='store',
        dest='init_file',
        metavar='FILENAME',
        help='Creates an empty .db file in Word Castle format.',
        type=str
    )
    return parser


def db_init(path):
    """
    Creates a new .db file in Word Castle format.
    :param path: Path of .db file
    :return: (Connection, Cursor)
    """
    if os.path.exists(path):
        if input(f'WARNING: DB file {path} already exists. Proceed? (Y/n)').lower() == 'n':
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
