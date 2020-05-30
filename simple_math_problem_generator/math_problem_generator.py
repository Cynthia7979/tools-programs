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

    def __repr__(self):
        return f"{self.question}={self.answer}"


def main():
    global type_config, global_config
    cli_args = sys.argv[1:]  # Get command line arguments, if any
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
            problem_output_format, answer_output_format, *_ = list(json.load(f).values())
        f_problem = open(os.path.join(output_path, 'problems.txt'), 'w', encoding='utf-8')
        f_answer = open(os.path.join(output_path, 'answers.txt'), 'w', encoding='utf-8')

        for i in range(num):
            q_type = random.choices(QUESTION_TYPES, weights=type_weights)[0]  # Randomly choose a question type
            problem = q_type()  # Call the question type function
            if global_config['pretty_output']:
                f_problem.write(problem_output_format.format(content=pretty(problem.question), no=i+1))
                f_answer.write(answer_output_format.format(content=pretty(problem.answer), no=i+1))
            else:
                f_problem.write(problem_output_format.format(content=str(problem.question), no=i+1))
                f_answer.write(answer_output_format.format(content=str(problem.answer), no=i+1))
    else:  # Interactive (shell) mode
        while True:
            q_type = random.choices(QUESTION_TYPES, weights=type_weights)[0]  # Randomly choose a question type
            problem = q_type()  # Call the question type function
            pprint(problem.question)  # "Ask" the question
            users_answer = input('Write your answer here, "quit" to quit: ')

            if users_answer == 'quit':
                break
            answer_is_right = False
            if users_answer and users_answer.strip():  # Not empty string
                try:
                    users_answer = sympify(users_answer)  # Convert user's answer to SymPy Expression
                except SympifyError:  # Answer can't be converted
                    print(f'Your input can\'t be recognized, attempting the workaround instead...')
                    problem.answer = str(problem.answer)  # Convert problem's answer to str
            if users_answer == problem.answer:
                print('Correct.')
            else:
                print('Incorrect.')
                pprint('The right answer is: '+str(problem.answer))
            print('-'*20)


def combine_configurations(higher_priority: dict, lower_priority: dict):
    """
    `combine_configurations({'a':1}, {'a':2, 'b':3}) -> {'a':1, 'b':3}`
    :param higher_priority: Configurations that should be saved when conflict occurs.
    :param lower_priority: Configurations that should be overwritten when conflict occurs.
    :return: Combined configurations (dict)
    """
    result = higher_priority
    for k in lower_priority.keys():
        if k not in result.keys():
            result[k] = lower_priority[k]
    return result


def load_configuration_file(path):
    """
    Load configurations as dict from the specified file.
    :param path: File.
    :return: dict
    """
    with open(path) as f:
        try:
            j = json.load(f)
        except Exception as e:
            print(f'Error when trying to load file "{path}":')
            raise e
    return j


def random_numbers(no_of_numbers, frequent_interval=4):  # Took from simple generator
    interval = random.gauss(frequent_interval, 0.5)
    results = []
    for n in range(no_of_numbers):
        results.append(random.uniform(10**interval, 10**(interval+1)))
    return results


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


def random_term(interval=None, maximum_terms=None, denominator_interval=None, float_precision=None, configuration_of=None,
                int_=True, float_=True, frac=True, expression=True):  # TODO: 支持随机字母(abc...xyz)
    value_types = []
    if int_: value_types.append("int")
    if float_: value_types.append('float')
    if frac: value_types.append('frac')
    if expression: value_types.append('expression')
    type_of_term = random.choice(value_types)
    if type_of_term == 'int':
        return random.randint(*interval)
    elif type_of_term == 'float':
        return random_float(interval, float_precision)
    elif type_of_term == 'frac':
        return random_float(interval, denominator_interval)
    elif type_of_term == 'expression':
        return f'({simple_computation(maximum_terms, configuration_of).question})'


"""
Problem-returning functions
-----------------
* Parameters: Configurations can be done by editing `config/problems.json`. 只有内部调用时可使用关键词参数。
* Returns: One Problem object.

Random numbers can be got using the three functions above.
"""


def simple_computation(maximum_terms:int=None, configuration_of='simple_computation'):
    """
    Simple 4-operand computations
    移除了分数项，因为除法运算会表示为分数
    禁用了括号（random_term的expression参数），因为会导致溢出
    :return: Problem object
    """
    func_config = combine_configurations(type_config[configuration_of], global_config)
    if maximum_terms: func_config['maximum_terms'] = maximum_terms
    number_of_terms = random.randint(2, func_config['maximum_terms'])

    question = str(random_term(
        interval=func_config['interval'],
        denominator_interval=func_config["denominator_interval"],
        float_precision=func_config['float_precision'],
        frac=False,
        expression=False
    ))
    # type_of_first_term = random.choice(VALUE_TYPES)
    # if type_of_first_term == 'int':
    #     first_term = random.randint(*func_config["interval"])
    # elif type_of_first_term == 'float':
    #     first_term = random_float(func_config["interval"], func_config["float_precision"])
    # else:
    #     raise ValueError(f'Unexpected type of term: {type_of_first_term}')
    # question = str(first_term)

    for term_number in range(number_of_terms):
        # type_of_term = random.choice(VALUE_TYPES)
        # if type_of_term == 'int':
        #     term = random.randint(*func_config["interval"])
        # elif type_of_term == 'float':
        #     term = random_float(func_config["interval"], func_config["float_precision"])
        # else:
        #     raise ValueError(f'Unexpected type of term: {type_of_term}')

        question += random.choice(['+', '-', '*', '/'])+str(random_term(
                                                    interval=func_config['interval'],
                                                    denominator_interval=func_config["denominator_interval"],
                                                    float_precision=func_config['float_precision'],
                                                    frac=False,
                                                    expression=False
                                                    ))

    answer = sympify(question).round(func_config['float_precision'])
    question = sympify(question, evaluate=False)
    problem = Problem(question, answer)
    return problem


def perfect_square_trinomial():
    """
    TODO
    完全平方式展开

    (ex_a, ex_b)**2
    :return: Problem object
    """
    ex_a = random_term()



#  Global constants
QUESTION_TYPES = [simple_computation]
VALUE_TYPES = ['int', 'float']


if __name__ == '__main__':
    main()
