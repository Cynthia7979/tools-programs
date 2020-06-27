import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from scipy.optimize import curve_fit

DATA_PATH = 'getHistory.html'
DATA_PATH_NEW = 'FAutoGlobalDailyList.json'


def read_data():
    data_processed = []
    # 0     1           2       3       4           5           6
    # date  confirmed   new     cured   deceased    deathrate   curerate
    data_x = []  # Date
    data_y = []  # Confirmed

    # Previous data (https://www.ncovchina.com/data/getHistory.html)
    # with open(DATA_PATH) as f:
    #     soup = BeautifulSoup(f.read())
    # data_raw = json.loads(soup.find('body').string)
    # for row in data_raw:
    #     month, day = row['date'].split('.')
    #     confirmed, suspected, cured, deceased = row['confirm'], row['suspect'], row['heal'], row['dead']
    #     int_date = int(month)*31 + int(day)
    #     data_processed.append([int_date, confirmed, suspected, cured, deceased])
    #     data_x.append(int_date)
    #     data_y.append(confirmed)
    # return data_processed, data_x, data_y

    # New data (https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalDailyList)
    with open(DATA_PATH_NEW) as f:
        data_raw = json.load(f)
    pprint(data_raw)
    for row in data_raw['data']['FAutoGlobalDailyList']:
        month, day = row['date'].split('.')
        confirmed, deceased, drate, cured, crate, new = row['all'].values()
        int_date = int(month)*31 + int(day)
        data_processed.append([int_date, confirmed, new, cured, deceased, drate, crate])
        data_x.append(int_date)
        data_y.append(confirmed)
    return data_processed, data_x, data_y


def plot_data(x, y, ax=plt, **kwargs):
    ax.plot(x, y, **kwargs)


def f(x, a):
    return np.power(a,x)


def func(x, a, b):
    return x**a + b


def main():
    rcParams['font.family'] = 'SimHei'
    fig, axes1 = plt.subplots()
    plt.xlabel('日期')
    plt.ylabel('确诊病例数')
    fig, axes2 = plt.subplots()
    plt.xlabel('日期')
    plt.ylabel('确诊病例数')
    fig, axes3 = plt.subplots()
    plt.xlabel('日期')
    plt.ylabel('确诊病例数')
    data, dx, dy = read_data()
    # dx, dy = dx[:50], dy[:50]
    pprint(dx, compact=True)
    pprint(dy, compact=True)

    axes1.set_title('全球新冠肺炎累计确诊数据')
    plot_data(dx, dy, ax=axes1, label='原始数据')

    # y1 = f(dx, 1.0788)
    # pprint(y1, compact=True)
    # plot_data(dx, y1, ax=axes, label='1.0788')
    #
    # y2 = f(dx, 1.08)
    # plot_data(dx, y2, ax=axes, label='1.08')
    #
    # y3 = f(dx, 1.07)
    # plot_data(dx, y3, ax=axes, label='1.07')
    #
    # y4 = f(dx, 1.0785)
    # plot_data(dx, y4, ax=axes, label='1.0785')

    axes2.set_title('新冠肺炎累计确诊数据拟合曲线')
    popt, pcov = curve_fit(func, dx, dy)
    y = [func(i, popt[0], popt[1]) for i in dx]
    axes2.plot(dx, dy, label='原始数据')
    axes2.plot(dx, y, 'r--', label='拟合数据')
    print(popt)

    axes3.set_title('新冠肺炎确诊数据预测')
    ex = np.arange(59, 300)
    popt, pcov = curve_fit(func, dx, dy)
    # popt数组中，三个值分别是待求参数a,b,c
    ey = [func(i, popt[0], popt[1]) for i in ex]
    axes3.plot(dx, dy, label='原始数据')
    axes3.plot(ex, ey, 'r--', label='预测数据')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
