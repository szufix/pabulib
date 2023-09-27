import csv
import os

from tqdm import tqdm

from _glossary import NAMES
import sys
import statistics
import ast
from _utils import *

import matplotlib.pyplot as plt
import numpy as np

from scipy import stats

nice_name = {
    'mes': 'MES',
    'greedy': "Greedy",
    'greedy_cost_sat': 'GreedyAV',
    'greedy_cardinality_sat': 'GreedyCost',
    'phragmen': 'Phragmén',
    'mes_phragmen': 'MES (+Ph.)',



    'warszawa_2021': 'Warsaw 2021',
    'warszawa_2022': 'Warsaw 2022',
    'warszawa_2023': 'Warsaw 2023',
    'krakow_2020': 'Kraków 2020',
    'krakow_2021': 'Kraków 2021',
    'krakow_2022': 'Kraków 2022',
}

def get_name(region):
    if region in ['krakow_2020', 'krakow_2021', 'krakow_2022']:
        return 'Score'
    elif region in ['warszawa_2020', 'warszawa_2021', 'warszawa_2022', 'warszawa_2023']:
        return 'Votes'


def import_values(region, name, method, r):
    name = name.replace('.pb', '')
    path = f"games/{region}/{name}_{method}_{r}.csv"

    costs = {}
    last_costs = {}
    winners = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            id_ = str(row['id'])
            cost = float(row['cost'])
            last_cost = float(row['last_cost'])
            winner = int(row['winner'])
            costs[id_] = cost
            last_costs[id_] = last_cost
            winners[id_] = winner

    return costs, last_costs, winners


def print_game_plot(region, name, instance, profile, _costs, _last_costs,
                    _original_winners, _winners, r):
    fig, ax = plt.subplots()

    support = []
    costs = []
    last_costs = []
    winners = []
    original_winners = []

    for c in instance:
        support.append(get_supporters(profile, c))
        winners.append(_winners[c.name])
        original_winners.append(_original_winners[c.name])
        costs.append(_costs[c.name])
        last_costs.append(_last_costs[c.name])

    ordered_costs = sort_by_indexes(costs, support, True)
    ordered_max_costs = sort_by_indexes(last_costs, support, True)
    ordered_winners = sort_by_indexes(winners, support, True)
    ordered_original_winners = sort_by_indexes(original_winners, support, True)
    ordered_support = sort_by_indexes(support, support, True)

    # winning_pos = [i for i in range(len(winning_costs))]
    # losing_pos = [i+len(winning_costs) for i in range(len(losing_costs))]

    for i in range(len(ordered_costs)):
        if ordered_winners[i]:
            color = 'royalblue'
        else:
            color = 'indianred'

        if ordered_max_costs[i] > ordered_costs[i]:
            plt.bar(i, ordered_costs[i], color=color, alpha=0.9)
            plt.bar(i, ordered_max_costs[i], color=color, alpha=0.5)
        else:
            plt.bar(i, ordered_max_costs[i], color=color, alpha=0.9)

        plt.bar(i, ordered_costs[i], fill=None, alpha=1, edgecolor='black')
        # plt.bar(i, ordered_max_costs[i], color=color, alpha=0.5)
        # plt.bar(i, ordered_max_costs[i], color=color, alpha=0.5)
        if ordered_original_winners[i]:
            plt.plot(i, ordered_costs[i], marker="D", linestyle="", alpha=1, color="black")
        # plt.bar(i, ordered_costs[i], color=color, alpha=alpha_1)
        #
        # plt.bar(str(ordered_support[i]), ordered_max_costs[i], color=color, alpha=alpha_2)
        # plt.bar(str(ordered_support[i]), ordered_costs[i], color=color, alpha=alpha_1)
        # plt.bar(str(ordered_support[i]), ordered_costs[i], fill=None, alpha=1, edgecolor='black')

    MAX_COST = int(instance.budget_limit)
    plt.ylim([0, 0.25*MAX_COST*1.02])

    # ax.set_xticklabels([str(ordered_support[i]) for i in range(len(ordered_support))])
    # ax.set_xticklabels(ordered_support)

    # plt.locator_params(axis="x", nbins=10)
    nbins = 8
    step = int((len(ordered_support)-1)/nbins)
    ticks = [i*step for i in range(nbins+1)]
    labels = [ordered_support[i] for i in ticks]

    plt.xticks(ticks=ticks, labels=labels, rotation=90, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel(get_name(region), fontsize=18)
    plt.ylabel('Cost', fontsize=18)
    plt.title(f'{nice_name.get(rule, rule)} ({nice_name.get(region, region)} | {NAMES[region][name]})',
              fontsize=16)
    name = name.replace('.pb', '')
    plt.savefig(f'images/games/{region}/{name}_{rule}_{r}', dpi=200, bbox_inches='tight')
    plt.close()
    # plt.show()



if __name__ == "__main__":

    num_rounds = 10000

    rules = [
        'greedy_cost_sat',
        'greedy_cardinality_sat',
        'phragmen',
        # 'mes_phragmen',
            ]

    if len(sys.argv) < 2:
        regions = [
            'warszawa_2023',
            # 'warszawa_2022',
            # 'warszawa_2021',

            # 'krakow_2022',
            # 'krakow_2021',
            # 'krakow_2020',
            # 'wieliczka_2023'
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

                instance, profile = import_election(region, name)
                original_winners_list = compute_winners(instance, profile, rule)
                original_winners = {}
                for p in instance:
                    if p in original_winners_list:
                        original_winners[p.name] = 1
                    else:
                        original_winners[p.name] = 0

                for r in tqdm(range(num_rounds+1)):
                    r=10000
                    if r % 10 == 0:

                        costs, last_costs, winners = import_values(region, name, rule, r)

                        print_game_plot(region, name, instance, profile,
                                          costs, last_costs, original_winners, winners, r)
                    break
