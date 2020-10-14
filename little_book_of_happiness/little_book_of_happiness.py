from time import sleep
from base64 import b64encode
from random import randint


def printw(phrase):
    sleep(0.1)
    phrase = phrase.split('\n')
    for p in phrase:
        print(p)
        sleep(0.3)


LITTLE_BOOK_OF_HAPPINESS = [
    """I made a little book of happiness to treasure
those happy moments.""",
    """This mock-up latency seems very satisfying. I
like it.""",
    """Do you know what force-revived turret-cubes are called?
FrankenTurrets.""",
    """Look - There's a rainbow in the sky."""
]

i = 0

printw('')
printw('LITTLE_BOOK_OF_HAPPINESS, '+b64encode('HAPPINESS_'+str(randint(1000,100000))))
printw('==========================================')
while True:
    if i >= len(LITTLE_BOOK_OF_HAPPINESS):
        printw('')
        printw('- END OF DISK -')
        selection = raw_input('Play again? (Y/n)  ').lower()
        if selection == 'n':
            break
        else:
            i = 0
            printw('')
    printw(LITTLE_BOOK_OF_HAPPINESS[i])
    _ = raw_input('>  ')
    i += 1



