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

import matplotlib.ticker as ticker
from scipy import stats

def compute_analytical_equilibrium_of_greedy_cardinality_sat(region, name):

    instance, profile = import_election(region, name)

    total_support = get_total_support(profile)

    last_costs = {p.name: instance.budget_limit * get_supporters(profile, p)/ total_support for p in instance}

    return last_costs


def compute_analytical_equilibrium_of_mes(region, name):

    instance, profile = import_election(region, name)

    money_unit = float(instance.budget_limit / len(profile))

    support = []
    projects = []
    for c in instance:
        support.append(get_supporters(profile, c))
        projects.append(c)
    ordered_projects = sort_by_indexes(projects, support, True)

    last_costs = {p.name: 0 for p in instance}

    q = 1
    while True:
        print(q)
        q = q+1

        p = ordered_projects[0]

        last_cost = 0

        for i, v in enumerate(profile):

            if p.name in v:
                last_cost += money_unit
                v.clear()

        # recount the votes
        support = []
        projects = []
        for c in instance:
            support.append(get_supporters(profile, c))
            projects.append(c)
        ordered_projects = sort_by_indexes(projects, support, True)

        last_costs[p.name] = last_cost

        print(p.name, last_cost, p.cost)
        # print(sum(support))

        if sum(support) == 0:
            break


    return last_costs


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
                    _original_winners, _winners, r, _eq_costs):
    fig, ax = plt.subplots()

    support = []
    costs = []
    last_costs = []
    winners = []
    original_winners = []
    eq_costs = []

    for c in instance:
        support.append(get_supporters(profile, c))
        winners.append(_winners[c.name])
        original_winners.append(_original_winners[c.name])
        costs.append(_costs[c.name])
        last_costs.append(_last_costs[c.name])
        eq_costs.append(_eq_costs[c.name])

    ordered_costs = sort_by_indexes(costs, support, True)
    ordered_max_costs = sort_by_indexes(last_costs, support, True)
    ordered_winners = sort_by_indexes(winners, support, True)
    ordered_original_winners = sort_by_indexes(original_winners, support, True)
    ordered_eq_costs = sort_by_indexes(eq_costs, support, True)
    ordered_support = sort_by_indexes(support, support, True)


    msize = int(280/len(ordered_costs))**2

    tshift = instance.budget_limit * (0.0003 + int(280/len(ordered_costs))/2000)

    # winning_pos = [i for i in range(len(winning_costs))]
    # losing_pos = [i+len(winning_costs) for i in range(len(losing_costs))]

    for i in range(len(ordered_costs)):
        if ordered_winners[i]:
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

        if ordered_original_winners[i]:
            plt.scatter(i, ordered_costs[i]+tshift, marker="^", alpha=1, color="black", s=msize)
            # plt.scatter(i, -10000, marker="x", alpha=1, color="black", s=8)

        # plt.scatter(i, ordered_eq_costs[i], marker="o", alpha=1, color="violet", s=msize)
        plt.scatter(i, ordered_eq_costs[i], marker="o", alpha=1, color="peru", s=msize)
        plt.scatter(i, ordered_eq_costs[i], marker="o", alpha=1, color="black", s=msize/16)


        # plt.bar(i, ordered_costs[i], color=color, alpha=alpha_1)
        #
        # plt.bar(str(ordered_support[i]), ordered_max_costs[i], color=color, alpha=alpha_2)
        # plt.bar(str(ordered_support[i]), ordered_costs[i], color=color, alpha=alpha_1)
        # plt.bar(str(ordered_support[i]), ordered_costs[i], fill=None, alpha=1, edgecolor='black')

    MAX_COST = int(instance.budget_limit)
    plt.ylim([0, 0.45*MAX_COST*1.02])

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

    plt.xticks(ticks=ticks, labels=labels, rotation=90, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('Number of votes', fontsize=20)
    plt.ylabel('Cost (in millions)', fontsize=20)
    # plt.title(f'{nice_name.get(rule, rule)} ({nice_name.get(region, region)} | {NAMES[region][name]})',
    #           fontsize=20)
    plt.title(f'{nice_name.get(rule, rule)}', fontsize=24)
    name = name.replace('.pb', '')
    plt.savefig(f'images/games/{region}/{name}_{rule}_{r}', dpi=200, bbox_inches='tight')
    plt.close()
    # plt.show()



if __name__ == "__main__":

    num_rounds = 10000

    rules = [
        # 'greedy_cost_sat',
        'greedy_cardinality_sat',
        # 'phragmen',
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

                    r = 10000

                    if r % 10 == 0:

                        costs, last_costs, winners = import_values(region, name, rule, r)

                        if rule == 'mes_phragmen':
                            eq_costs = compute_analytical_equilibrium_of_mes(region, name)
                        elif rule == 'greedy_cardinality_sat':
                            eq_costs = compute_analytical_equilibrium_of_greedy_cardinality_sat(region, name)

                        print_game_plot(region, name, instance, profile,
                                          costs, last_costs, original_winners, winners, r,
                                        eq_costs)

                    break

# 70217