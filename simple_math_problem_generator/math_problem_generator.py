import random
import sys, os
import json
from sympy.abc import *
from sympy import *
from sympy.core.sympify import SympifyError


class Problem(object):
    """
    Class for single math problems
    """
    def __init__(self, question, answer=None):
        """
        :param question: Question represented as SymPy expression
        :param answer: Answer represented either as SymPy expression or int/float value
        """
        self.question = question
        self.answer = answer

    def set_answer(self, answer):
        self.answer = answer

    def __repr__(self):
        return f"{self.question}={self.answer}"


def main():
    global type_config, global_config
    # Get command line arguments, if any
    cli_args = sys.argv[1:]
    # Load config files
    type_weights = list(load_configuration_file('./config/weights.json').values())
    type_config = load_configuration_file('./config/problems.json')
    global_config = load_configuration_file('./config/config.json')

    init_printing()

    if cli_args:  # Output (command line) mode
        num = int(cli_args[0])
        if len(cli_args) > 1:
            output_path = cli_args[1]
        else:
            output_path = './output/'

        with open('./config/output.json') as f:
            problem_output_format, answer_output_format = list(json.load(f).values())
        f_problem = open(os.path.join(output_path, 'problems.txt'), 'w', encoding='utf-8')
        f_answer = open(os.path.join(output_path, 'answers.txt'), 'w', encoding='utf-8')
        for i in range(num):
            q_type = random.choices(QUESTION_TYPES, weights=type_weights)[0]
            problem = q_type()
            if global_config['pretty_output']:
                f_problem.write(problem_output_format.format(content=pretty(problem.question), no=i+1))
                f_answer.write(answer_output_format.format(content=pretty(problem.answer), no=i+1))
            else:
                f_problem.write(problem_output_format.format(content=str(problem.question), no=i+1))
                f_answer.write(answer_output_format.format(content=str(problem.answer), no=i+1))
    else:  # Interactive (shell) mode
        while True:
            q_type = random.choices(QUESTION_TYPES, weights=type_weights)[0]
            problem = q_type()
            pprint(problem.question)
            users_answer = input('Write your answer here, "quit" to quit: ')

            if users_answer == 'quit':
                break

            answer_is_right = False
            if users_answer and users_answer.strip():  # Not empty string
                try:
                    users_answer = sympify(users_answer)  # Convert to SymPy Expression
                    if users_answer == problem.answer:
                        answer_is_right = True
                except SympifyError:  # If answer can't be converted
                    print(f'Your input can\'t be recognized, attempting the workaround instead...')
                    if users_answer == str(problem.answer):  # Then convert the answer to str
                        answer_is_right = True
            else:
                answer_is_right = False  # Just to be clear..
            if answer_is_right:
                print('Correct.')
                print('-'*20)
            else:
                print('Incorrect.')
                pprint('The right answer is: '+str(problem.answer))
                print('-'*20)


def random_numbers(no_of_numbers, frequent_interval=4):  # Took from simple generator
    interval = random.gauss(frequent_interval, 0.5)
    results = []
    for n in range(no_of_numbers):
        results.append(random.uniform(10**interval, 10**(interval+1)))
    return results


def combine_configurations(higher_priority: dict, lower_priority: dict):
    result = higher_priority
    for k in lower_priority.keys():
        if k not in result.keys():
            result[k] = lower_priority[k]
    return result


def load_configuration_file(path):
    with open(path) as f:
        try:
            j = json.load(f)
        except Exception as e:
            print(f'Error when trying to load file "{path}":')
            raise e
    return j


def random_float(interval, float_prec):
    result = str(random.randint(interval[0], interval[1] - 1))+'.'
    for i in range(float_prec):
        if i != float_prec - 1:
            result += str(random.randint(0, 9))
        else:
            result += str(random.randint(1, 9))
    return float(result)


def random_frac(interval, denom_interval):
    denominator = random.randint(*denom_interval)
    numerator = random.randint(denominator * interval[0], denominator * interval[1])
    return Rational(numerator, denominator)


def simple_computation():
    """
    Simple 4-operand computations
    :return: Problem object
    """
    func_config = combine_configurations(type_config['simple_computation'], global_config)
    number_of_terms = random.randint(2, global_config['maximum_terms'])

    # first_term
    type_of_term = random.choice(VALUE_TYPES)
    if type_of_term == 'int':
        first_term = random.randint(*func_config["interval"])
    elif type_of_term == 'float':
        first_term = random_float(func_config["interval"], func_config["float_precision"])
    # elif type_of_term == 'frac':
    #     first_term = random_frac(func_config["interval"], func_config["denominator_interval"])
    else:
        raise ValueError(f'Unexpected type of term: {type_of_term}')

    question = str(first_term)
    for i in range(number_of_terms):
        type_of_term = random.choice(VALUE_TYPES)
        if type_of_term == 'int':
            term = random.randint(*func_config["interval"])
        elif type_of_term == 'float':
            term = random_float(func_config["interval"], func_config["float_precision"])
        # elif type_of_term == 'frac':
        #     term = random_frac(func_config["interval"], func_config["denominator_interval"])
        else:
            raise ValueError(f'Unexpected type of term: {type_of_term}')

        operation = random.choice(['+', '-', '*', '/'])
        question += operation + str(term)
    answer = sympify(question).round(func_config['float_precision'])
    question = sympify(question, evaluate=False)
    problem = Problem(question, answer)
    return problem


#  Global constants
QUESTION_TYPES = [simple_computation]
VALUE_TYPES = [
    'int', 'float', #'frac'
                ]


if __name__ == '__main__':
    main()
