import matplotlib.pyplot as plt
import math


def estimate(func, init_cond: tuple, step=0.1, lower_x=-1, upper_x=1, prec=3):
    """

    :param func: The differential equation in the form of f(x, y) => dy/dx
    :param init_cond: The initial condition. Currently only accepts (0, y)
    :param step: The step size. Defaults to 0.1.
    :param lower_x: The lower boundary of the range to be drawn. Currently does nothing and the range is [0, upper_x]
    :param upper_x: The upper boundary of the range to be drawn.
    :param prec: Precision after the float point for x and y
    :return: Two lists `x` and `y`
    """
    x = [init_cond[0]]
    y = [init_cond[1]]
    assert upper_x > lower_x, 'The upper X coordinate must be greater than the lower X coordinate'
    assert callable(func), 'The function you passed is not callable.'
    current_x, current_y = init_cond
    while current_x < upper_x:
        current_y += func(current_x, current_y) * step
        current_x += step
        current_y = round(current_y, prec)
        current_x = round(current_x, prec)
        y.append(current_y)
        x.append(current_x)
    x = [round(i, prec) for i in x]
    y = [round(j, prec) for j in y]
    # print(x, y)
    return x, y


def show_estimate(x, y):
    plt.plot(x, y)
    plt.show()


def estimate_at(x_value, x: list, y: list):
    if x_value in x:
        return y[x.index(x_value)]
    else:  # Use slope to estimate y
        p1_ind = tuple(idx for idx, value in enumerate(x) if value < x_value)[-1]  # Smallest x that is greater than 1.0
        p2_ind = tuple(idx for idx, value in enumerate(x) if value > x_value)[0]   # Largest x that is less than 1.0
        slope = (y[p2_ind] - y[p1_ind]) / (x[p2_ind] - x[p1_ind])
        x_diff = 1.0 - x[p1_ind]
        y_diff = x_diff * slope
        return y[p1_ind] + y_diff


def show_step_size_against_estimate(lower_step, upper_step, meta_step, predef_estimate, x_value, prec=4):
    """
    Displays a graph of step size against estimated y at given x.
    :param lower_step: The lower boundary of step. Positive float.
    :param upper_step: The upper boundary of step (inclusive). Positive float. Must be greater than `lower_step`
    :param meta_step: The value to increase step size by. Positive float.
    :param predef_estimate: A predefined estimate() function. Common usage: `lambda step: estimate(..., step=step)`
    :param x_value: The given x value to estimate y value at.
    :param prec: The precision (number of digits after the float point) at which step size is rounded to. Defaults to 4.
    """
    assert callable(predef_estimate), 'Predefined estimate() function must be callable'
    assert 0 < lower_step < upper_step, \
        'Boundaries of step must be positive, and upper step must be greater than lower step'
    steps = []
    estimations = []
    current_step_size = lower_step
    while current_step_size <= upper_step:
        steps.append(current_step_size)
        estimations.append(estimate_at(x_value, *predef_estimate(current_step_size)))
        current_step_size += meta_step
        current_step_size = round(current_step_size, prec)
    plt.plot(steps, estimations)
    plt.show()


if __name__ == '__main__':
    # show_step_size_against_estimate(
    #     lower_step=0.025,
    #     upper_step=1.0,
    #     meta_step=0.025,
    #     predef_estimate=lambda step: estimate(lambda y: y*(4-y)*(y-6), (0,5), step=step, upper_x=2, prec=3),
    #     x_value=1.0)
    # x_lst, y_lst = estimate(lambda y: y*(4-y)*(y-6), (0, 4), upper_x=2, prec=2, step=0.01)

    x_lst, y_lst = estimate_two_args(lambda x, y: x**2 + y**2, (0, 1), upper_x=1, prec=2, step=0.1)
    print(estimate_at(0.4, x_lst, y_lst))

    show_estimate(x_lst, y_lst)
