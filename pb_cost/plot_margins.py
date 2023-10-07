import csv
import os
from _glossary import NAMES
import sys
import statistics
import ast
from _utils import *

import matplotlib.pyplot as plt
import numpy as np

from scipy import stats
import matplotlib.ticker as ticker

nice_name = {
    'mes': 'MES',
    'greedy': "Greedy",
    'greedy_cost_sat': 'BasicAV',
    'greedy_cardinality_sat': 'AV/Cost',
    'phragmen': 'Phragmén',
    'mes_phragmen': 'MES-Cost/Ph',
    'mes_card_phragmen': 'MES-Apr/Ph',


    'warszawa_2021': 'Warsaw 2021',
    'warszawa_2022': 'Warsaw 2022',
    'warszawa_2023': 'Warsaw',
    'krakow_2020': 'Kraków 2020',
    'krakow_2021': 'Kraków 2021',
    'krakow_2022': 'Kraków 2022',
}

def get_name(region):
    if region in ['krakow_2020', 'krakow_2021', 'krakow_2022']:
        return 'Score'
    elif region in ['warszawa_2020', 'warszawa_2021', 'warszawa_2022', 'warszawa_2023']:
        return 'Number of votes'


def import_values(region, name, method, limit=10, type=None):
    name = name.replace('.pb', '')
    path = f"margins/{type}/{region}/{name}_{method}.csv"

    costs = {}
    max_costs = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            id_ = str(row['id'])
            cost = float(row['cost'])
            max_cost = float(row['max_cost'])
            costs[id_] = cost
            max_costs[id_] = max_cost

    return costs, max_costs

def sort_by_indexes(lst, indexes, reverse=False):
  return [val for (_, val) in sorted(zip(indexes, lst), key=lambda x: \
          x[0], reverse=reverse)]


def get_supporters(profile, c):
    support = 0
    for vote in profile:
        if c.name in vote:
            support += 1
    return support


def print_margin_plot(region, name, instance, profile,
                              winning_costs, winning_max_costs,
                              losing_costs, losing_max_costs, limit=1.):

    fig, ax = plt.subplots(figsize=(8, 4))

    support = []
    costs = []
    max_costs = []
    winning = []

    for c in instance:
        support.append(get_supporters(profile, c))
        if c.name in winning_costs:
            winning.append(True)
            costs.append(winning_costs[c.name])
            max_costs.append(winning_max_costs[c.name])
        elif c.name in losing_costs:
            winning.append(False)
            costs.append(losing_costs[c.name])
            max_costs.append(losing_max_costs[c.name])

    ordered_costs = sort_by_indexes(costs, support, True)
    ordered_max_costs = sort_by_indexes(max_costs, support, True)
    ordered_winning = sort_by_indexes(winning, support, True)
    ordered_support = sort_by_indexes(support, support, True)



    # winning_pos = [i for i in range(len(winning_costs))]
    # losing_pos = [i+len(winning_costs) for i in range(len(losing_costs))]


    for i in range(len(ordered_costs)):
        if ordered_winning[i]:
            # color = 'royalblue'
            color = 'forestgreen'
        else:
            color = 'indianred'

        if ordered_max_costs[i] > ordered_costs[i]:
            plt.bar(i, ordered_costs[i], color=color, alpha=0.9)
            plt.bar(i, ordered_max_costs[i], color=color, alpha=0.5)
        else:
            plt.bar(i, ordered_max_costs[i], color=color, alpha=0.9)

        plt.bar(i, ordered_costs[i], fill=None, alpha=1, edgecolor='black')


    # for i in range(len(ordered_costs)):
    #     if ordered_winning[i]:
    #         color = 'royalblue'
    #         alpha_1 = 0.9
    #         alpha_2 = 0.5
    #     else:
    #         color = 'indianred'
    #         alpha_1 = 0.5
    #         alpha_2 = 0.9
    #
    #     plt.bar(i, ordered_max_costs[i], color=color, alpha=alpha_2)
    #     plt.bar(i, ordered_costs[i], color=color, alpha=alpha_1)
    #     plt.bar(i, ordered_costs[i], fill=None, alpha=1, edgecolor='black')
        #
        # plt.bar(str(ordered_support[i]), ordered_max_costs[i], color=color, alpha=alpha_2)
        # plt.bar(str(ordered_support[i]), ordered_costs[i], color=color, alpha=alpha_1)
        # plt.bar(str(ordered_support[i]), ordered_costs[i], fill=None, alpha=1, edgecolor='black')
    print(region, instance.budget_limit)
    plt.ylim([0, limit*int(instance.budget_limit)*1.02])

    # ax.set_xticklabels([str(ordered_support[i]) for i in range(len(ordered_support))])
    # ax.set_xticklabels(ordered_support)

    # plt.locator_params(axis="x", nbins=10)
    nbins = 8
    step = int((len(ordered_support)-1)/nbins)
    ticks = [i*step for i in range(nbins+1)]
    labels = [ordered_support[i] for i in ticks]

    scale_y = 1e6
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
    ax.yaxis.set_major_formatter(ticks_y)

    plt.xticks(ticks=ticks, labels=labels, rotation=90, fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel('Number of votes', fontsize=24)
    plt.ylabel('Cost (in millions)', fontsize=24)
    # plt.title(f'{nice_name.get(rule, rule)} ({nice_name.get(region, region)} | {NAMES[region][name]})',
    #           fontsize=20)
    plt.title(f'{nice_name.get(rule, rule)} | {NAMES[region][name]}', fontsize=28)
    name = name.replace('.pb', '')
    plt.savefig(f'images/margins/{region}/{name}_{rule}', dpi=200, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":

    rules = [
        'greedy_cost_sat',
        'greedy_cardinality_sat',
        'phragmen',
        'mes_phragmen',
        'mes_card_phragmen'
            ]

    if len(sys.argv) < 2:
        regions = [
            'warszawa_2023',
            # 'wieliczka_2023',
            # 'amsterdam'
        ]
    else:
        regions = [str(sys.argv[1])]

    for region in regions:

        boxplots = []
        labels = []
        budget_ratios = []
        medians = []
        ds = []

        for i, name in enumerate(NAMES[region]):
            print(name)
            for rule in rules:

                winning_costs, winning_max_costs = import_values(region, name, rule, type='winning')
                losing_costs, losing_max_costs = import_values(region, name, rule, type='losing')
                instance, profile = import_election(region, name)

                print_margin_plot(region, name, instance, profile,
                                  winning_costs, winning_max_costs,
                                  losing_costs, losing_max_costs,
                                  # limit=0.25
                                  # limit=0.18
                                  limit=0.21
                                  )
