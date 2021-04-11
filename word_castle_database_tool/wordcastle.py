import argparse
import sys
import sqlite3
import xml.etree.ElementTree as ET

DEBUG_ARGS = '--youdao test.xml'.split()


def main():
    parser = argparse.ArgumentParser(
        usage='Generate word castle .db files with YouDao XML or custom words'
    )
    parser.add_argument(
        '-t', '--txt',
        action='store',
        dest='txt_path',
        help='Path of txt file'
    )
    parser.add_argument(
        '-y', '--youdao',
        action='store',
        dest='yd_path',
        help='Path of YouDao wordbook file. This overwrites the txt file.',
        type=str
    )
    if len(sys.argv) == 1:  # Testing
        print('WARNING: You did not pass any arguments. This will parse', DEBUG_ARGS)
        args = parser.parse_args(DEBUG_ARGS)
    else:
        args = parser.parse_args()

    if args.yd_path:
        assert args.yd_path.endswith('.xml'), 'YouDao file must be in XML format.'
        xml2db(args.yd_path)


def xml2db(path):
    f = ET.parse(path)
    print(f.getroot())


if __name__ == '__main__':
    main()
