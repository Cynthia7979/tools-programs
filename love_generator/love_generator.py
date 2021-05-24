"""
Love Generator. Provides Authentic Love from n=1 to n=7.
"""

from time import sleep


def love(n):
    MIDDLE = 1
    layers = []
    width = (2*n)+1

    # First layer
    if n % 2 == 1:  # n is odd
        top = (n+1)//2
    else:
        top = (n+2)//2
    wrap = (width - MIDDLE - 2*top)//2
    layers.append(' '*wrap + '*'*top + ' '*MIDDLE + '*'*top + ' '*wrap)

    # Second layer
    layers.append('*'*width)

    # Third to n-1 layers
    for ventricle in range(0, n-3):
        size = width-2*ventricle
        wrap = (width-size)//2
        layers.append(' '*wrap + '*'*size)

    # Last layer
    layers.append(' '*(width//2) + '*' + ' '*(width//2))

    return layers


def say(*sentences, patience=0.5):
    for sentence in sentences:
        print(sentence)
        sleep(patience)


def write(line, patience=0.5):
    for letter in line:
        print(letter, end='')
        sleep(patience)


if __name__ == '__main__':
    for ai in range(1, 8):
        print(ai)
        say(*love(ai))
        print()
    write('LOVE.')
