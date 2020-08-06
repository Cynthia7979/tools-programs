import requests
import random
import sys, os


def main(file='source.txt', debug=False):
    f = open(file, encoding='utf-8')
    lines = [s.strip('\n') for s in f.readlines()]
    choices = []
    for i, line in enumerate(lines):
        splitted = line.split()
        choice = splitted[0]
        if len(splitted) > 1:
            try:
                frequency = sum((int(j) for j in splitted[1:]))
            except TypeError:
                raise TypeError(f'Spotted non-integer frequency in source (line {i})')
        else:
            frequency = 1
        choices.extend([choice]*frequency)
    number_of_choices = len(choices)-1
    try:
        final_result = get_random_number(0, number_of_choices)
    except requests.exceptions.ConnectionError:
        print('Cannot connect to RANDOM.ORG. Using pseudo-random instead...')
        final_result = random.randint(0,number_of_choices)
    print(choices[final_result])
    if debug: print(choices)


def get_random_number(minimum, maximum, number_of_numbers=1, base=10):
    random_number = int(requests.get(f"https://www.random.org/integers/?num={number_of_numbers}&min={minimum}&max={maximum}&col=5&base={base}&format=plain&rnd=new").text)
    return random_number


if __name__ == '__main__':
    try:
        _, file_, *debug_ = sys.argv
        debug_ = False if debug_ == ['False'] else True
    except ValueError:
        file_ = 'source.txt'
        debug_ = False
    main(file=file_, debug=debug_)
