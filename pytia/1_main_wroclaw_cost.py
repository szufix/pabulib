
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt

from glossary import NAMES

def print_cost(city, year, savefig=False):


    data = []

    num_selected = 0
    max_cost = 0

    for name in NAMES[f'{city}_{year}c']:

        # print(name)
        path = f'pabulib_877/{name}'
        instance, profile = parse_pabulib(path)

        for project in instance:
            cost = float(project.cost)
            if cost > max_cost:
                max_cost = cost
            data.append(cost)

        for p in instance.project_meta:
            if instance.project_meta[p]['selected'] == '1':
                num_selected += 1

    print(f'num_selected: {num_selected}')

    # print(data)

    base = 250000
    bars = [0 for _ in range(0, 11)]
    for d in data:
        for i in range(10):
            # print(d)
            if d < i*base:
                bars[i] += 1
                break
    # count how many project have max cost
    max_cost_count = 0
    for d in data:
        if d == max_cost:
            max_cost_count += 1
    print(max_cost_count/len(data))

    keynote_blue = '#007AFF'

    # UPDATE FOR OTHER CITIES
    bins = [0,250000,500000,750000,1000000,1250000,1500000,1750000,2000000,2250000]
    # plt.hist(data, bins=10, range=(0, 2000000))
    plt.hist(data, bins=bins, color=keynote_blue, edgecolor='black')

    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    # add names on the x axis in the middle of the bars
    X_names = [
        '[0-0.25)',
        '[0.25-0.5)',
        '[0.5-0.75)',
        '[0.75-1)',
        '[1-1.25)',
        '[1.25-1.5)',
        '[1.5-1.75)',
        '[1.75-2)',
        '=2M',
    ]
    #
    ticks = [i*base + base/2 for i in range(0, 9)]
    plt.xticks(ticks, X_names, rotation=55)

    # increase the size of values in the y axis
    plt.tick_params(axis='y', labelsize=20)
    plt.tick_params(axis='x', labelsize=12)

    # Define the Keynote-like color palette

    # keynote_colors = ['#007AFF', '#FF2D55', '#FF9500', '#4CD964', '#5856D6', '#FFCC00', '#8E8E93']

    # Create the histogram with specified colors for each bin
    # n, bins, patches = plt.hist(data, bins=bins, edgecolor='black')

    # Apply colors to each bar
    # for patch, color in zip(patches, keynote_colors):
    #     patch.set_facecolor(color)

    if savefig:
        plt.savefig(f'sscw/{city}_{year}c', bbox_inches='tight', dpi=200)
    plt.close()

    # plt.show()

    # plt.hist(data, bins=10, range=(1, 11))
    # plt.hist(data)

    # ticks = [i + 0.5 for i in range(0, 11)]
    # plt.xticks(ticks, [str(i) for i in range(0, 11)])
    # plt.ylim([0,70000])

    # plt.title("Histogram of lengths of votes")
    # plt.savefig(f'{city}_{year}c')
    # plt.show()


def print_cost_all(city, year, savefig=False):


    data = []

    num_selected = 0
    max_cost = 0

    for name in NAMES[f'{city}_{year}c']:

        # print(name)
        path = f'pabulib_877/{name}'
        instance, profile = parse_pabulib(path)

        for project in instance:
            cost = float(project.cost)
            if cost > max_cost:
                max_cost = cost
            data.append(cost)


    # print(data)

    base = 250000
    bars = [0 for _ in range(0, 11)]
    for d in data:
        for i in range(10):
            # print(d)
            if d < i*base:
                bars[i] += 1
                break
    # count how many project have max cost
    max_cost_count = 0
    for d in data:
        if d == max_cost:
            max_cost_count += 1
    print(max_cost_count/len(data))

    keynote_blue = '#007AFF'

    # UPDATE FOR OTHER CITIES
    # plt.hist(data, bins=10, range=(0, 2000000))
    plt.hist(data, bins=10, color=keynote_blue, edgecolor='black')

    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    # add names on the x axis in the middle of the bars
    # X_names = [
    #     '[0-0.25)',
    #     '[0.25-0.5)',
    #     '[0.5-0.75)',
    #     '[0.75-1)',
    #     '[1-1.25)',
    #     '[1.25-1.5)',
    #     '[1.5-1.75)',
    #     '[1.75-2)',
    #     '=2M',
    # ]
    # #
    # ticks = [i*base + base/2 for i in range(0, 9)]
    # plt.xticks(ticks, X_names, rotation=55)

    plt.xticks([], [])

    # increase the size of values in the y axis
    plt.tick_params(axis='y', labelsize=20)
    plt.tick_params(axis='x', labelsize=12)

    # Define the Keynote-like color palette

    # keynote_colors = ['#007AFF', '#FF2D55', '#FF9500', '#4CD964', '#5856D6', '#FFCC00', '#8E8E93']

    # Create the histogram with specified colors for each bin
    # n, bins, patches = plt.hist(data, bins=bins, edgecolor='black')

    # Apply colors to each bar
    # for patch, color in zip(patches, keynote_colors):
    #     patch.set_facecolor(color)

    if savefig:
        plt.savefig(f'sscw/{city}_{year}c_noaxis', bbox_inches='tight', dpi=200)
    plt.close()



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
    print_cost_all('krakow', 2023, savefig=True)
