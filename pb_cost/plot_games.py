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


def import_values(region, name, method):
    name = name.replace('.pb', '')
    path = f"games/{region}/{name}_{method}.csv"

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


def sort_by_indexes(lst, indexes, reverse=False):
  return [val for (_, val) in sorted(zip(indexes, lst), key=lambda x: \
          x[0], reverse=reverse)]


def get_supporters(profile, c):
    support = 0
    for vote in profile:
        if c.name in vote:
            support += 1
    return support


def print_game_plot(region, name, instance, profile, _costs, _last_costs, _winners):
    fig, ax = plt.subplots()

    support = []
    costs = []
    last_costs = []
    winners = []


    for c in instance:
        support.append(get_supporters(profile, c))
        winners.append(_winners[c.name])
        costs.append(_costs[c.name])
        last_costs.append(_last_costs[c.name])

    ordered_costs = sort_by_indexes(costs, support, True)
    ordered_max_costs = sort_by_indexes(last_costs, support, True)
    ordered_winning = sort_by_indexes(winners, support, True)
    ordered_support = sort_by_indexes(support, support, True)

    # winning_pos = [i for i in range(len(winning_costs))]
    # losing_pos = [i+len(winning_costs) for i in range(len(losing_costs))]

    for i in range(len(ordered_costs)):
        if ordered_winning[i] and ordered_max_costs[i] > ordered_costs[i]:
            color = 'olivedrab'
            alpha_1 = 0.9
            alpha_2 = 0.5
        elif ordered_winning[i]:
            color = 'royalblue'
            alpha_1 = 0.5
            alpha_2 = 0.9
        else:
            color = 'indianred'
            alpha_1 = 0.5
            alpha_2 = 0.9

        plt.bar(i, ordered_max_costs[i], color=color, alpha=alpha_2)
        plt.bar(i, ordered_costs[i], color=color, alpha=alpha_1)
        plt.bar(i, ordered_costs[i], fill=None, alpha=1, edgecolor='black')
        #
        # plt.bar(str(ordered_support[i]), ordered_max_costs[i], color=color, alpha=alpha_2)
        # plt.bar(str(ordered_support[i]), ordered_costs[i], color=color, alpha=alpha_1)
        # plt.bar(str(ordered_support[i]), ordered_costs[i], fill=None, alpha=1, edgecolor='black')

    MAX_COST = int(instance.budget_limit)
    plt.ylim([0, MAX_COST*1.02])

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
    plt.savefig(f'images/games/{region}/{name}_{rule}', dpi=200, bbox_inches='tight')
    # plt.show()


def get_budget_ratio(region, name):
    path = f"data/{region}/{name}"

    election = Election()
    election.read_from_files(path)

    budget = election.budget
    sum_costs = sum([c.cost for c in election.profile])
    budget_ratio = round(sum_costs / budget, 2)
    # print(f'{budget}, {sum_costs}, {budget_ratio}')
    return budget_ratio
    # return len(election.profile)


def diversity_of_votes(region, name):
    election = import_election(region, name)
    total_similarity = 0
    for c1 in election.profile.values():
        for c2 in election.profile.values():
            a1 = set(c1.keys())
            a2 = set(c2.keys())
            similarity = len(a1.intersection(a2)) / len(a1.union(a2))
            total_similarity += similarity
    return total_similarity / len(election.profile) / len(election.profile)


if __name__ == "__main__":

    rules = [
        # 'greedy_cost_sat',
        'greedy_cardinality_sat',
        # 'phragmen',
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

                costs, last_costs, winners = import_values(region, name, rule)

                instance, profile = import_election(region, name)

                print_game_plot(region, name, instance, profile,
                                  costs, last_costs, winners)

