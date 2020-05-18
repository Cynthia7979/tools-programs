import random
from sympy import *


class Problem(object):
    """
    Base class for single math problems
    """
    def __init__(self, problem, answer=None):
        """

        :param problem:
        :param answer: None
        """
        self.problem = problem

def random_numbers(no_of_numbers, frequent_interval=4):  # Took from simple generator
    interval = random.gauss(frequent_interval, 0.5)
    results = []
    for n in range(no_of_numbers):
        results.append(random.uniform(10**interval, 10**(interval+1)))
    return results

