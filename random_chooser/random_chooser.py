import requests
import random
import sys, os


def main(file='source.txt', how_much=1, repeated=True, debug=False, **overflow):
    # Process argvs
    how_much = int(how_much)
    repeated = True if repeated=='True' else False
    debug = True if debug=='True' else False

    # Process choices and weights
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
    sample_size = len(choices)-1
    
    # Get random numbers

    result = []

    if repeated:
        try:
            result += get_random_numbers(0, sample_size, number_of_numbers=how_much)
        except requests.exceptions.ConnectionError:
            print('WARNING: Cannot connect to RANDOM.ORG. Using pseudo-randomness instead...')
            result += [random.randint(0,sample_size) for i in range(how_much)]
    else:
        if how_much > sample_size:
            print('WARNING: Number of numbers is larger than sample size. There WILL be repeated results.')
            for i in range(how_much // sample_size):
                try:
                    result += get_random_sequence(0, sample_size, number_of_numbers=sample_size)
                except requests.exceptions.ConnectionError:
                    print('WARNING: Cannot connect to RANDOM.ORG. Using pseudo-randomness instead...')
                    result += [random.randint(0,sample_size) for i in range(sample_size)]
            how_much = how_much % sample_size
        try:
            result += get_random_sequence(0, sample_size, number_of_numbers=how_much)
        except requests.exceptions.ConnectionError:
            print('WARNING: Cannot connect to RANDOM.ORG. Using pseudo-randomness instead...')
            result += [random.randint(0, sample_size) for i in range(how_much)]
        
    print('Results')
    print('----------')
    print('\n'.join([choices[int(random_index)] for random_index in result]))
    if debug: print('pool:', choices)


def get_random_numbers(minimum, maximum, number_of_numbers=1, base=10):
    random_number = requests.get(f"https://www.random.org/integers/?num={number_of_numbers}&min={minimum}&max={maximum}&col=1&base={base}&format=plain&rnd=new").text
    return random_number.split('\n')[:-1]


def get_random_sequence(minimum, maximum, number_of_numbers=1):
    # This function (and the URL below) is used to generate non-repeating numbers
    random_sequence = requests.get(f'https://www.random.org/sequences/?min={minimum}&max={maximum}&col=1&format=plain&rnd=new').text
    return random_sequence.split('\n')[:number_of_numbers]


if __name__ == '__main__':
    kwargs = {'file': 'source.txt',
              'how_much': 1,
              'repeated': True,
              'debug': False}
    for argv in sys.argv[1:]:
        key, value = argv.split('=')
        kwargs[key] = value
    main(**kwargs)
