
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


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
    # for i in range(1, 16):
    #     print(f'{i}, ', end='')
    # print('')
    # print(bars[1:16])
    print(bars[15]/sum(bars))



def print_warszawa_citywide(year):


    data = []

    for name in NAMES[f'warszawa_{year}c']:

        # print(name)
        path = f'pabulib_877/{name}'
        instance, profile = parse_pabulib(path)

        for v in profile:
            data.append(len(v))

    bars = [0 for _ in range(0, 11)]
    for d in data:
        bars[d] += 1
    # for i in range(1, 11):
    #     print(f'{i}, ', end='')
    # print('')
    # print(bars[1:11])

    # print(bars[10]/sum(bars))
    print(bars[1]/sum(bars))

def print_trend_max():
    X = ['2020', '2021', '2022', '2023', '2024']

    Y = [0.4870907853922349,
         0.685763146643865,
         0.6404214983873747,
         0.6744905201257224,
         0.7377051358713707]

    keynote_blue = '#007AFF'

    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))

    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    plt.yticks(fontsize=16)
    plt.xticks(fontsize=18)

    plt.ylim([0.45, 0.75])

    plt.plot(X, Y, marker='o', color=keynote_blue)
    plt.savefig(f'sscw/warszawa_trend_c', bbox_inches='tight', dpi=200)
    plt.show()

def print_trend_min():
    X = ['2020', '2021', '2022', '2023', '2024']

    Y = [0.4870907853922349,
         0.685763146643865,
         0.6404214983873747,
         0.6744905201257224,
         0.7377051358713707]

    keynote_blue = '#007AFF'

    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))

    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    plt.yticks(fontsize=16)
    plt.xticks(fontsize=18)

    plt.ylim([0.45, 0.75])

    plt.plot(X, Y, marker='o', color=keynote_blue)
    plt.savefig(f'sscw/warszawa_trend_c', bbox_inches='tight', dpi=200)
    plt.show()

if __name__ == "__main__":

    # print_warszawa_districts('2020')
    # print_warszawa_districts('2021')
    # print_warszawa_districts('2022')
    # print_warszawa_districts('2023')
    # print_warszawa_districts('2024')

    print_warszawa_citywide('2020')
    print_warszawa_citywide('2021')
    print_warszawa_citywide('2022')
    print_warszawa_citywide('2023')
    print_warszawa_citywide('2024')

