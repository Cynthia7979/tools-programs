"""
Love Generator:
    love(3)
        *·*
        ·*·
    love(5)
        **·**
        *****
        ··*··
    love(7)
        ·**·**·
        *******
        ·*****·
        ···*···
    love(9)
        ·***·***·
        *********
        ··*****··
        ····*····
    love(11)
        ··***·***··
        ***********
        ··*******··
        ····***····
        ·····*·····
"""
from time import sleep


def postponed_print(*strs, time=0.5):
    for s in strs:
        print(s)
        sleep(time)


def postponed_write(s, time=0.5):
    for letter in s:
        print(letter, end='')
        sleep(time)


if __name__ == '__main__':
    postponed_print(
        '     *** ***  ',
        '    ********* ',
        '    ********* ',
        '      *****   ',
        '        *     '
    )
    postponed_write('LOVE.')
