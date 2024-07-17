
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

    keynote_blue = '#007AFF'
    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    plt.hist(data, bins=10, range=(1, 11), color=keynote_blue, edgecolor='black')

    ticks = [i + 0.5 for i in range(0, 11)]
    plt.xticks(ticks, [str(i) for i in range(0, 11)])
    # plt.ylim([0, 50000])

    # plt.title("Histogram of lengths of votes")
    plt.savefig(f'sscw/warszawa_{year}c', bbox_inches='tight', dpi=200)
    plt.show()



def print_wroclaw_citywide(year):


    data = []

    for name in NAMES[f'wroclaw_{year}c']:

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

    keynote_blue = '#007AFF'
    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    plt.hist(data, bins=10, range=(1, 11), color=keynote_blue, edgecolor='black')

    ticks = [i + 0.5 for i in range(0, 11)]
    plt.xticks(ticks, [str(i) for i in range(0, 11)])
    # plt.ylim([0, 50000])

    # plt.title("Histogram of lengths of votes")
    plt.savefig(f'sscw/wroclaw_{year}c', bbox_inches='tight', dpi=200)
    plt.show()


def print_amsterdam_citywide(year):


    data = []

    for name in NAMES[f'amsterdam_{year}']:

        print(name)
        path = f'pabulib_877/{name}'
        instance, profile = parse_pabulib(path)

        for v in profile:
            data.append(len(v))

    # bars = [0 for _ in range(0, 11)]
    # for d in data:
    #     bars[d] += 1
    # for i in range(1, 11):
    #     print(f'{i}, ', end='')
    # print('')
    # print(bars[1:11])
    # print(bars[10]/sum(bars))

    keynote_blue = '#007AFF'
    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    plt.hist(data, bins=50, range=(1, 51), color=keynote_blue, edgecolor='black')

    x_ticks = [str(i) for i in range(1, 51)]
    for i in range(len(x_ticks)):
        if i % 5 != 0:
            x_ticks[i] = ''

    ticks = [i + 0.5 for i in range(1, 51)]
    plt.xticks(ticks, x_ticks)
    # plt.ylim([0, 50000])

    # plt.title("Histogram of lengths of votes")
    plt.savefig(f'sscw/amsterdam_{year}', bbox_inches='tight', dpi=200)
    plt.show()


if __name__ == "__main__":

    # print_warszawa_districts('2020')
    # print_warszawa_districts('2021')

    # print_warszawa_citywide('2020')

    # print_warszawa_citywide('2024')
    # print_wroclaw_citywide('2023')
    print_amsterdam_citywide('252')
