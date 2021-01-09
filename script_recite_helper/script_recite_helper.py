# -*- encoding: utf-8 -*-
import os

SPLITER = "："
NAME_KEYWORD = "萍"
NON_KEYWORDS = ('侍萍',)
FILENAME = './script.txt'

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def main():
    with open(FILENAME, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\r\n')
            speaker = line[:line.find(SPLITER)]
            if NAME_KEYWORD in speaker and not any([non_keyword in speaker for non_keyword in NON_KEYWORDS]):
                _ = input('[YOUR LINE]')
                delete_previous_line()
                print(WARNING+line+ENDC)
            else:
                _ = input()
                delete_previous_line()
                print(line)
    os.system('cls' if os.name=='nt' else 'clear')
    print('-- La fine --')


def delete_previous_line():
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)


if __name__ == "__main__":
    main()
