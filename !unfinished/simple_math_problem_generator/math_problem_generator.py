import sys, os
import json
from sympy.abc import *
from sympy import *
from sympy.core.sympify import SympifyError
from random import choice, choices, randint, uniform, gauss


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
    type_weights = list(load_configuration_file('config/weights.json').values())
    type_config = load_configuration_file('config/problems.json')
    global_config = load_configuration_file('config/config.json')

    init_printing()

    if cli_args:  # Output (command line) mode
        num = int(cli_args[0])
        if len(cli_args) > 1:
            output_path = cli_args[1]
        else:
            output_path = 'output/'

        with open('config/output.json') as f:
            problem_output_format, answer_output_format, *_ = list(json.load(f).values())
        f_problem = open(os.path.join(output_path, 'problems.txt'), 'w', encoding='utf-8')
        f_answer = open(os.path.join(output_path, 'answers.txt'), 'w', encoding='utf-8')

        for i in range(num):
            q_type = choices(QUESTION_TYPES, weights=type_weights)[0]  # Randomly choose a question type
            problem = q_type()  # Call the question type function
            if global_config['pretty_output']:
                f_problem.write(problem_output_format.format(content=pretty(problem.question), no=i+1))
                f_answer.write(answer_output_format.format(content=pretty(problem.answer), no=i+1))
            else:
                f_problem.write(problem_output_format.format(content=str(problem.question), no=i+1))
                f_answer.write(answer_output_format.format(content=str(problem.answer), no=i+1))
    else:  # Interactive (shell) mode
        while True:
            try:
                q_type = choices(QUESTION_TYPES, weights=type_weights)[0]  # Randomly choose a question type
            except ValueError:  # If the number of weights does not match the population
                raise ValueError('The number of weights does not match the population. Please check config/weights.json')
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


def process_raw_symbol(raw_symbol):
    processed_symbol = None
    if raw_symbol == 'random':
        _rand = randint(0, 1)
        if _rand == 0:
            processed_symbol = choice((a,b,c,x,y,z))
        elif _rand == 1:
            processed_symbol = None
    elif not raw_symbol:
        processed_symbol = None
    else:
        processed_symbol = symbols(raw_symbol)
    return processed_symbol


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
    interval = gauss(frequent_interval, 0.5)
    results = []
    for n in range(no_of_numbers):
        results.append(uniform(10**interval, 10**(interval+1)))
    return results


def random_float(interval, float_prec):
    result = str(randint(interval[0], interval[1] - 1))+'.'
    for i in range(float_prec):
        if i != float_prec - 1:
            result += str(randint(0, 9))
        else:
            result += str(randint(1, 9))
    return float(result)


def random_frac(interval, denom_interval):
    denominator = randint(*denom_interval)
    numerator = randint(denominator * interval[0], denominator * interval[1])
    return Rational(numerator, denominator)


def random_term(interval=None, maximum_terms=None, denominator_interval=None, float_precision=None, configuration_of=None,
                int_=True, float_=True, frac=True, expression=True, symbol=None):  # TODO: 支持随机字母(abc...xyz)
    value_types = []
    if int_: value_types.append("int")
    if expression: value_types.append('expression')
    if not symbol:
        if float_: value_types.append('float')
        if frac: value_types.append('frac')
    type_of_term = choice(value_types)
    print(f'Chosen {type_of_term}')
    if type_of_term == 'int':
        term = randint(*interval)
    elif type_of_term == 'float':
        term = random_float(interval, float_precision)
    elif type_of_term == 'frac':
        term = random_frac(interval, denominator_interval)
    elif type_of_term == 'expression':
        term = simple_computation(maximum_terms, configuration_of).question
    print(term, symbol, type(symbol))
    term = Mul(term, symbol) if symbol else term
    return term


"""
Problem-returning functions
-----------------
* Parameters: Configurations can be done by editing `config/problems.json`. 只有内部调用时可使用关键词参数。
* Returns: One Problem object.

Random numbers can be got using the three functions above.
"""


def simple_computation(maximum_terms:int=None, configuration_of=None):
    """
    Simple 4-operand computations
    移除了分数项，因为除法运算会表示为分数
    禁用了括号（random_term的expression参数），因为会导致溢出
    :return: Problem object
    """
    if not configuration_of: configuration_of = 'simple_computation'
    func_config = combine_configurations(type_config[configuration_of], global_config)
    if maximum_terms:
        func_config['maximum_terms'] = maximum_terms
    func_config['symbol'] = process_raw_symbol(func_config['symbol'])

    number_of_terms = randint(2, func_config['maximum_terms'])
    random_term_kwargs = {'interval':func_config['interval'],
                          'denominator_interval': func_config['denominator_interval'],
                          'float_precision': func_config['float_precision'],
                          'frac': False,
                          'expression': False,
                          'symbol': func_config['symbol']}
    str_question = str(random_term(**random_term_kwargs))

    for term_number in range(number_of_terms):
        #                      operand                         term
        str_question += choice(['+', '-', '*', '/'])+str(random_term(**random_term_kwargs))
    answer = sympify(str_question) if func_config['symbol'] else sympify(str_question).round(func_config['float_precision'])
    question = sympify(str_question, evaluate=False)
    problem = Problem(question, answer)
    return problem


def perfect_square_trinomial():
    """
    TODO
    完全平方式展开

    (ex_a+-ex_b)**2
    :return: Problem object
    """
    func_config = combine_configurations(type_config['perfect_square_trinomial'], global_config)
    random_term_kwargs = {
        'interval': func_config['interval'],
        'maximum_terms': func_config['maximum_terms'],
        'denominator_interval': func_config['denominator_interval'],
        'float_precision': func_config['float_precision'],
        'configuration_of': 'perfect_square_trinomial',
        'symbol': process_raw_symbol(func_config['symbol']),
    }
    ex_a, ex_b = random_term(**random_term_kwargs), random_term(**random_term_kwargs)
    _rand = randint(0,1)
    if _rand == 0: ex_b = -ex_b
    question = UnevaluatedExpr((ex_a+ex_b)**2)
    answer = UnevaluatedExpr(ex_a**2 + 2*ex_a*ex_b + ex_b**2)
    return Problem(question, answer)



#  Global constants
QUESTION_TYPES = [simple_computation, perfect_square_trinomial]


if __name__ == '__main__':
    main()
