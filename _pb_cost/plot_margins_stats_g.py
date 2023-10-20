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
    'greedy_cardinality_sat': 'AVoverCost',
    'phragmen': 'Phragmén',
    'mes_phragmen': 'MES (+Ph.)',



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





def import_values_game(region, name, method, r):
    name = name.replace('.pb', '')
    path = f"games/{region}/{name}_{method}_{r}.csv"

    costs = {}
    last_costs = {}
    winners = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            id_ = str(row['idx'])
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


def print_margin_stats(region, name, instance, profile,
                              winning_costs, winning_max_costs,
                              losing_costs, losing_max_costs, rule,):
    fig, ax = plt.subplots()

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

    plus = []
    minus = []

    for i in range(len(ordered_costs)):
        diff = ordered_max_costs[i] - ordered_costs[i]
        if diff > 0:
            plus.append(diff)
        elif diff < 0:
            minus.append(diff)

    plus = np.array(plus)
    minus = np.array(minus)
    line = f'{rule} & {convert(np.mean(plus))} $\pm{convert(np.std(plus))}$ &'
    line += f'{convert(np.mean(minus))} $\pm{convert(np.std(minus))}$ \\\\'
    print(line)



if __name__ == "__main__":

    rules = [
        # 'greedy_cost_sat',
        'greedy_cardinality_sat',
        'phragmen',
        'mes_phragmen',
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

                winning_costs, winning_max_costs = import_values(region, name, rule, type='winning',  add='10000')
                losing_costs, losing_max_costs = import_values(region, name, rule, type='losing',  add='10000')

                instance, profile = import_election(region, name)

                print_margin_stats(region, name, instance, profile,
                                  winning_costs, winning_max_costs,
                                  losing_costs, losing_max_costs, rule,
                                   )

