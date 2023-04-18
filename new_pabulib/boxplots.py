import csv
import os
from glossary import NAMES
import sys
import statistics
import ast
from _utils import *

import matplotlib.pyplot as plt
import numpy as np

from scipy import stats

from pabutools.model import Election

nice_name = {
    'warszawa_2021': 'Warszawa (elections held in 2020)',
    'warszawa_2022': 'Warszawa (elections held in 2021)',
    'warszawa_2023': 'Warszawa (elections held in 2022)',
    'krakow_2020': 'Kraków (elections held in 2020)',
    'krakow_2021': 'Kraków (elections held in 2021)',
    'krakow_2022': 'Kraków  (elections held in 2022)',
}


def import_values(region, name, method, limit=10, type=None):
    name = name.replace('.pb', '')
    path = f"margins/{type}/{region}/{name}_{method}.csv"

    values = []
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            value = float(row['ratio'])
            if value > limit:
                value = limit
            values.append(value)

    return values


def print_boxplots(region, boxplots, labels, limit=10, type=None):
    fig, ax = plt.subplots()

    positions = []
    for i in range(int(len(boxplots) / 2)):
        positions.append(i * 4)
        positions.append(i * 4 + 1)

    bplot = ax.boxplot(boxplots, labels=labels, patch_artist=True, positions=positions)

    for median in bplot['medians']:
        median.set_color('black')
        median.set_linewidth(3)

    for i, bplot in enumerate(bplot['boxes']):
        if i % 2 == 0:
            color = 'blue'
        else:
            color = 'red'
        bplot.set_color(color)
        bplot.set_alpha(0.5)

    plt.xticks(rotation=90, fontsize=6)
    if limit > 1:
        plt.ylim([0, limit + 0.5])
    else:
        plt.ylim([0, limit])
    plt.yticks(fontsize=20)
    plt.ylabel('Ratio', fontsize=20)
    plt.title(nice_name[region], fontsize=20)
    plt.savefig(f'images/margins/{type}/{region}', dpi=200, bbox_inches='tight')
    plt.show()


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

    limit = 1
    type_ = 'losing'

    if len(sys.argv) < 2:
        regions = [
            # 'warszawa_2023',
            # 'warszawa_2022',
            # 'warszawa_2021',
            'krakow_2022',
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
            mes = import_values(region, name, 'mes', limit=limit, type=type_)
            boxplots.append(mes)
            labels.append(f'MES {NAMES[region][name]}')

            greedy = import_values(region, name, 'greedy', limit=limit, type=type_)
            boxplots.append(greedy)
            labels.append(f'Gr. {NAMES[region][name]}')

            budget_ratios.append(get_budget_ratio(region, name))
            medians.append(statistics.median(mes))
            # d = diversity_of_votes(region, name)
            # print(name, round(d, 4))
            # ds.append(d)

        print_boxplots(region, boxplots, labels, limit=limit, type=type_)

        print(round(stats.pearsonr(budget_ratios, medians)[0], 3))
        # plt.scatter(budget_ratios, medians)
        # plt.show()

        # print('AVG', round(stats.pearsonr(budget_ratios, ds)[0], 3))
