
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

    keynote_blue = '#007AFF'
    plt.hist(data, bins=15, range=(1, 16), color=keynote_blue, edgecolor='black')
    # plt.ylim([0,40000])


    ticks = [i + 0.5 for i in range(0, 16)]
    plt.xticks(ticks, [str(i) for i in range(0, 16)])

    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    # plt.ylim([0, 50000])

    # plt.title("Histogram of lengths of votes")
    plt.savefig(f'sscw/warszawa_{year}d', bbox_inches='tight', dpi=200)
    plt.show()


if __name__ == "__main__":

    # print_warszawa_districts('2020')
    print_warszawa_districts('2021')
