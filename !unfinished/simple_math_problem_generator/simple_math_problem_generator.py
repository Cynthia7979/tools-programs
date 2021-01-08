import random
from sympy import *


PREC = 0
FREQ_INTERVAL = 1


def main():
    while True:
        problems_and_answers = sum_calculation_problems(PREC, interval=FREQ_INTERVAL) +\
                               four_problems(PREC, interval=FREQ_INTERVAL)

        random.shuffle(problems_and_answers)
        for p, a in problems_and_answers:
            user_asw = input(p+' = ')
            if user_asw == str(a):
                print('Correct.')
            else:
                print('Incorrect.')
                print(f'Correct answer: {a}')
            print('----------------')


def output():
    problem_f = open('problems')


def random_numbers(no_of_numbers, frequent_interval=4):
    interval = random.gauss(frequent_interval, 0.5)
    results = []
    for n in range(no_of_numbers):
        results.append(random.uniform(10**interval, 10**(interval+1)))
    return results


def random_computation_problem(prec, interval=None, computation='random'):
    """

    :param prec: Float precision
    :param interval: None or int
    :param computation: 'random''+''-''*''/'
    :return: (str 'problem', int answer)
    """
    if computation == 'random':
        computation = random.choice(('+', '-', '*', '/'))
    if interval: num1, num2 = random_numbers(2, frequent_interval=interval)
    else: num1, num2 = random_numbers(2)
    num1, num2 = round(num1, prec), round(num2, prec)
    problem = f'{num1} {computation} {num2}'
    answer = round(eval(problem), prec)
    if computation == '/':
        additional_problem = f'{num2} {computation} {num1}'
        additional_answer = round(eval(problem), prec)
        return [(problem, answer), (additional_problem, additional_answer)]
    return [(problem, answer)]


def four_problems(prec, interval=None):
    return random_computation_problem(prec, interval, '+') +\
            random_computation_problem(prec, interval, '-') +\
            random_computation_problem(prec, interval, '*') +\
            random_computation_problem(prec, interval, '/')


def sum_calculation_problems(prec, interval=None):
    if interval: number_sequence = random_numbers(random.randint(5, 15), frequent_interval=interval)
    else: number_sequence = random_numbers(random.randint(5, 15))
    number_sequence = [round(i, prec) for i in number_sequence]
    corr_answ = sum(number_sequence)
    return [(f'Compute the sum of the following numbers:\n {number_sequence}', corr_answ)]


if __name__ == '__main__':
    main()
