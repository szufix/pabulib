
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt

from glossary import NAMES



def print_wieliczka_citywide(stanford_name):

    data = []



    path = f'stanford_data/{stanford_name}.pb'
    instance, profile = parse_pabulib(path)

    for v in profile:
        data.append(len(v))

    bars = [0 for _ in range(0, 6)]
    for d in data:
        if d>5:
            d=5
        bars[d] += 1
    for i in range(1, 6):
        print(f'{i}, ', end='')
    print('')
    print(bars[1:6])
    print(bars[-1]/sum(bars))

    X_names = [
        '1', '2', '3', '4', '5'
    ]
    #

    keynote_blue = '#007AFF'
    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 18

    plt.hist(data, bins=5, range=(1, 6), color=keynote_blue, edgecolor='black')

    ticks = [i + 0.5 for i in range(1, 6)]
    plt.xticks(ticks, X_names, fontsize=24)

    # plt.title("Histogram of lengths of votes")
    plt.savefig(f'stanford_img/{stanford_name}', bbox_inches='tight', dpi=200)
    plt.show()


if __name__ == "__main__":

    # print_cost('wroclaw', 2016)
    # print_cost('wroclaw', 2017)
    # print_cost('wroclaw', 2018)
    # print_cost('wroclaw', 2019)
    # print_cost('wroclaw', 2020)
    # print_cost('wroclaw', 2020, savefig=True)
    # print_cost('wroclaw', 2021)
    # print_cost('wroclaw', 2022)

    # print_cost_all('warszawa', 2024, savefig=True)
    # print_cost_all('wroclaw', 2023, savefig=True)
    # print_cost_all('amsterdam', 252, savefig=True)
    # print_cost_all('wieliczka', 2023, savefig=True)

    stanford_name = "Worldwide_Stanford_PB_Vallejo_2017_vote_approvals"
    stanford_name = "Worldwide_Stanford_PB_Cambridge_2019_vote_approvals"
    stanford_name = "Worldwide_Stanford_PB_Rochester_NY_2019_vote_rankings_clean"
    print_wieliczka_citywide(stanford_name)
