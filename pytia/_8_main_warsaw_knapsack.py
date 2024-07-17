
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt

from glossary import NAMES


def print_warsaw(year):

    data = []

    for name in NAMES[f'warszawa_{year}t']:

        print(name)
        path = f'pabulib_877/{name}'
        instance, profile = parse_pabulib(path)

        for v in profile:
            data.append(len(v))

    bars = [0 for _ in range(0, 15)]
    for d in data:
        if d>14:
            d=14
        bars[d] += 1
    for i in range(1, 11):
        print(f'{i}, ', end='')
    print('')
    print(bars[1:11])
    print(bars[1]/sum(bars))

    X_names = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'
    ]
    #

    keynote_blue = '#007AFF'
    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    plt.hist(data, bins=14, range=(1, 15), color=keynote_blue, edgecolor='black')

    ticks = [i + 0.5 for i in range(1, 15)]
    plt.xticks(ticks, X_names)
    # plt.ylim([0, 3500])

    # plt.title("Histogram of lengths of votes")
    plt.savefig(f'sscw/warszawa_{year}t', bbox_inches='tight', dpi=200)
    plt.show()



if __name__ == "__main__":

    print_warsaw(2019)
