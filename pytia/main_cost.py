
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt

from glossary import NAMES

def print_cost(city, year):


    data = []

    for name in NAMES[f'{city}_{year}c']:

        print(name)
        path = f'pabulib_877/{name}'
        instance, profile = parse_pabulib(path)

        for project in instance:
            data.append(float(project.cost))

    # print(data)

    base = 250000
    bars = [0 for _ in range(0, 11)]
    for d in data:
        for i in range(10):
            print(d)
            if d < i*base:
                bars[i] += 1
                break
    print(sorted(data))
    for i in range(1, 11):
        print(f'{i}, ', end='')
    print('')
    print(bars)
    print(61/len(data))

    # plt.hist(data, bins=10, range=(1, 11))
    # plt.hist(data)

    # ticks = [i + 0.5 for i in range(0, 11)]
    # plt.xticks(ticks, [str(i) for i in range(0, 11)])
    # plt.ylim([0,70000])

    # plt.title("Histogram of lengths of votes")
    # plt.savefig(f'{city}_{year}c')
    # plt.show()


if __name__ == "__main__":

    print_cost('wroclaw', 2020)
