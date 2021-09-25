import matplotlib.pyplot as plt


def estimate(func, init_cond: tuple, step=0.1, lower_x=-1, upper_x=1, prec=3):
    """

    :param func: The differential equation in the form of f(y) => y'
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
        current_y += func(current_y) * step
        y.append(current_y)
        current_x += step
        x.append(current_x)
    x = [round(i, prec) for i in x]
    y = [round(j, prec) for j in y]
    print(x, y)
    return x, y


def show_estimate(x, y):
    plt.plot(x, y)
    plt.show()


def estimate_at(x_value, x: list, y: list):
    return y[x.index(x_value)]


if __name__ == '__main__':
    x_lst, y_lst = estimate(lambda y: y*(4-y), (0, 2), upper_x=2, prec=2)
    print(estimate_at(1.0, x_lst, y_lst))

    show_estimate(x_lst, y_lst)
