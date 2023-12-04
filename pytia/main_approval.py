
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt

from glossary import NAMES


def print_warszawa_districts(year):

    data = []

    for name in NAMES[f'warszawa_{year}d']:

        print(name)
        path = f'pabulib_877/{name}'
        instance, profile = parse_pabulib(path)

        for v in profile:
            data.append(len(v))

    bars = [0 for _ in range(0, 16)]
    for d in data:
        bars[d] += 1
    for i in range(1, 16):
        print(f'{i}, ', end='')
    print('')
    print(bars[1:16])
    print(bars[15]/sum(bars))

    plt.hist(data, bins=15, range=(1, 16))
    plt.ylim([0,50000])


    ticks = [i + 0.5 for i in range(0, 16)]
    plt.xticks(ticks, [str(i) for i in range(0, 16)])

    plt.title("Histogram of lengths of votes")
    plt.savefig(f'warszawa_{year}d')
    plt.show()


def print_warszawa_citywide(year):


    data = []

    for name in NAMES[f'warszawa_{year}c']:

        print(name)
        path = f'pabulib_877/{name}'
        instance, profile = parse_pabulib(path)

        for v in profile:
            data.append(len(v))

    bars = [0 for _ in range(0, 11)]
    for d in data:
        bars[d] += 1
    for i in range(1, 11):
        print(f'{i}, ', end='')
    print('')
    print(bars[1:11])
    print(bars[10]/sum(bars))

    plt.hist(data, bins=10, range=(1, 11))

    ticks = [i + 0.5 for i in range(0, 11)]
    plt.xticks(ticks, [str(i) for i in range(0, 11)])
    plt.ylim([0,70000])

    plt.title("Histogram of lengths of votes")
    plt.savefig(f'warszawa_{year}c')
    plt.show()


def print_wieliczka_citywide(year):

    data = []

    for name in NAMES[f'wieliczka_{year}c']:

        print(name)
        path = f'pabulib_877/{name}'
        instance, profile = parse_pabulib(path)

        for v in profile:
            data.append(len(v))

    bars = [0 for _ in range(0, 11)]
    for d in data:
        if d>10:
            d=10
        bars[d] += 1
    for i in range(1, 11):
        print(f'{i}, ', end='')
    print('')
    print(bars[1:11])
    print(bars[1]/sum(bars))

    plt.hist(data, bins=10, range=(1, 11))

    ticks = [i + 0.5 for i in range(0, 11)]
    plt.xticks(ticks, [str(i) for i in range(0, 11)])
    # plt.ylim([0,70000])

    plt.title("Histogram of lengths of votes")
    plt.savefig(f'wieliczka_{year}c')
    plt.show()


if __name__ == "__main__":

    # print_warszawa_districts('2020')
    # print_warszawa_districts('2021')

    # print_warszawa_citywide('2020')
    # print_warszawa_citywide('2021')
    print_wieliczka_citywide(2023)
