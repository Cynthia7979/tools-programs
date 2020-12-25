import requests
import random
import sys, os


def main(file='source.txt', num=1, debug=False):
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
    final_result = []
    for i in range(num):
        try:
            final_result.append(get_random_number(0, number_of_choices))
        except requests.exceptions.ConnectionError:
            print('Cannot connect to RANDOM.ORG. Using pseudo-random instead...')
            final_result.append(random.randint(0,number_of_choices))
    print('\n'.join([choices[random_index] for random_index in final_result]))
    if debug: print('pool:', choices)


def get_random_number(minimum, maximum, number_of_numbers=1, base=10):
    random_number = int(requests.get(f"https://www.random.org/integers/?num={number_of_numbers}&min={minimum}&max={maximum}&col=5&base={base}&format=plain&rnd=new").text)
    return random_number


if __name__ == '__main__':
    file_ = 'source.txt'
    num_ = 1
    debug_ = False
    try:
        _, num_, *file_ = sys.argv
        num_ = int(num_)
        file_ = file_[0] if file_ else 'source.txt'
    except ValueError:
        pass
    main(file=file_, num=num_, debug=debug_)
