import csv
import os
import matplotlib.pyplot as plt
from glossary import NAMES
from matplotlib.transforms import Bbox
from matplotlib.markers import MarkerStyle
import sys
import statistics
import ast

from scipy import stats

from sklearn.manifold import MDS
import numpy as np

from PIL import Image
import math

from pabutools.rules import equal_shares, utilitarian_greedy
from pabutools.model import Election
nice_name = {
    'warszawa_2020': 'Warszawa 2020',
    'warszawa_2021': 'Warszawa 2021',
    'warszawa_2022': 'Warszawa 2022',
    'warszawa_2023': 'Warszawa 2023',
}

def import_values(region, name, method, limit=10):

    name = name.replace('.pb', '')
    path = f"margins/{region}/{name}_{method}.csv"

    values = []
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            value = float(row['ratio'])
            if value > limit:
                value = limit
            values.append(value)

    return values


def print_boxplots(region, boxplots, labels, limit=10):
    fig, ax = plt.subplots()

    positions = []
    for i in range(int(len(boxplots)/2)):
        positions.append(i*4)
        positions.append(i*4+1)

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
    plt.ylim([0,limit+0.5])
    plt.yticks(fontsize=20)
    plt.ylabel('Ratio', fontsize=20)
    plt.title(nice_name[region], fontsize=20)
    plt.savefig(f'images/margins/{region}', dpi=200, bbox_inches='tight')
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


if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import numpy as np

    instance_type = 'approval'
    distance_id = 'jaccard'
    limit = 50


    if len(sys.argv) < 2:
        regions = [
            'warszawa_2020',
            'warszawa_2021',
            'warszawa_2022',
            'warszawa_2023',
        ]
    else:
        regions = [str(sys.argv[1])]

    for region in regions:

        boxplots = []
        labels = []
        budget_ratios = []
        medians = []

        for i, name in enumerate(NAMES[region]):
            mes = import_values(region, name, 'mes', limit=limit)
            boxplots.append(mes)
            labels.append(f'MES {NAMES[region][name]}')

            greedy = import_values(region, name, 'greedy', limit=limit)
            boxplots.append(greedy)
            labels.append(f'Gr. {NAMES[region][name]}')

            budget_ratios.append(get_budget_ratio(region, name))
            medians.append(statistics.median(mes))

        print_boxplots(region, boxplots, labels, limit=limit)

        print(round(stats.pearsonr(budget_ratios, medians)[0], 3))
        plt.scatter(budget_ratios, medians)
        # plt.show()


# -0.521
# -0.623
# -0.532
# 0.086
