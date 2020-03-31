import requests
import sys, os


def main(file='source.txt', debug=False):
    f = open(file, encoding='utf-8')
    lines = [s.strip('\n') for s in f.readlines()]
    # choices = {}
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
    final_result = get_random_number(0, number_of_choices)
    print(choices[final_result])
    if debug: print(choices)


def get_random_number(minimum, maximum, number_of_numbers=1, base=10):
    random_number = int(requests.get(f"https://www.random.org/integers/?num={number_of_numbers}&min={minimum}&max={maximum}&col=5&base={base}&format=plain&rnd=new").text)
    return random_number


if __name__ == '__main__':
    main(debug=False)
