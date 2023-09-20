import copy
import csv
import os
import random

import matplotlib.pyplot as plt
from _glossary import NAMES
from matplotlib.transforms import Bbox
from matplotlib.markers import MarkerStyle
import sys
from tqdm import tqdm

import ast
from _glossary import *
from _utils import *

from scipy import stats

from sklearn.manifold import MDS
import numpy as np
# import mapel.elections as mapel
from PIL import Image
import math

from pabutools.election import parse_pabulib

from pabutools.election import Cost_Sat
from pabutools.rules import max_additive_utilitarian_welfare

plt.rcParams["font.family"] = "Times New Roman"


def get_max_cost(region, budget):
    # if region in ['krakow_2020', 'krakow_2021', 'krakow_2022']:
    #     return budget*0.4
    # elif region in ['warszawa_2020', 'warszawa_2021', 'warszawa_2022', 'warszawa_2023']:
    #     return budget*0.2
    return budget


def import_data(path):
    meta = {}
    projects = {}
    votes = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        section = ""
        header = []
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if str(row[0]).strip().lower() in ["meta", "projects", "votes"]:
                section = str(row[0]).strip().lower()
                header = next(reader)
            elif section == "meta":
                meta[row[0]] = row[1].strip()
            elif section == "projects":
                projects[row[0]] = {}
                for it, key in enumerate(header[1:]):
                    projects[row[0]][key.strip()] = row[it + 1].strip()
            elif section == "votes":
                votes[row[0]] = {}
                for it, key in enumerate(header[1:]):
                    votes[row[0]][key.strip()] = row[it + 1].strip()
    return meta, projects, votes


def jaccard_distance(ac1, ac2):
    if len(ac1.union(ac2)) != 0:
        return 1 - len(ac1.intersection(ac2)) / len(ac1.union(ac2))
    return 0


def compute_distances(projects, acs):
    distances = {project_id: {} for project_id in projects}

    for project_id_1 in projects:
        ac1 = acs[str(project_id_1)]
        for project_id_2 in projects:
            if project_id_2 == project_id_1:
                continue
            ac2 = acs[str(project_id_2)]
            distances[str(project_id_1)][str(project_id_2)] = jaccard_distance(ac1, ac2)
            # distances[str(project_id_2)][str(project_id_1)] = distances[str(project_id_1)][str(project_id_2)]

    return distances


def convert_distances(distances):
    new_distances = np.zeros([len(distances), len(distances)])
    for p1, project_id_1 in enumerate(distances):
        for p2, project_id_2 in enumerate(distances[project_id_1]):
            new_distances[p1][p2] = distances[project_id_1][project_id_2]
            new_distances[p2][p1] = new_distances[p1][p2]

    return new_distances


def merge_images(list_of_names=None, size=250, show=False, ncol=1, nrow=1,
                 region=None):
    images = []
    for i, name in enumerate(list_of_names):
        if 'blank' in name:
            images.append(Image.open(f'images/blank.png'))
        else:
            images.append(Image.open(f'images/{region}/{name}.png'))
    image1_size = images[0].size

    new_image = Image.new('RGB', (ncol * image1_size[0], nrow * image1_size[1]),
                          (size, size, size))

    for i in range(ncol):
        for j in range(nrow):
            try:
                new_image.paste(images[i + j * ncol], (image1_size[0] * i, image1_size[1] * j))
            except:
                pass

    new_image.save(f'images/{region}.png', "PNG", quality=85)
    if show:
        new_image.show()


def import_original_winners(projects):
    winners = set()
    for project_id in projects:
        # print(projects[project_id])
        if projects[project_id]['selected'] == '1':
            winners.add(project_id)
    return winners


def convert_winners(winners):
    new_winners = set()
    for w in winners:
        new_winners.add(w.id)
    return new_winners


def verify_cost(winners):
    total = 0
    for w in winners:
        total += w.cost
    print(total)


def _store_game_results_in_csv(region, name, method, results):
    name = name.replace('.pb', '')
    path = os.path.join(os.getcwd(), "games", region, f'{name}_{method}.csv')
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["id", "cost", "last_cost", "winner"])

        for r in results:
            writer.writerow([r,
                  results[r]['cost'],
                  results[r]['last_cost'],
                  results[r]['winner']])


# def get_winners(election, method):
#     if method == 'mes':
#         winners_tmp = equal_shares(election, completion='add1_utilitarian')
#         winners_tmp = convert_winners(winners_tmp)
#     elif method == 'greedy':
#         winners_tmp = utilitarian_greedy(election)
#         winners_tmp = convert_winners(winners_tmp)
#     return winners_tmp

#############################


def compute_iterative_game(region, name, method, num_rounds=100):
    A = []
    B = []
    C = []

    print("hello")

    instance, profile = import_election(region, name)

    results = {p.name: {'cost': p.cost, 'winner': 0} for p in instance}

    original_winners = compute_winners(instance, profile, method)

    for p in instance:
        if p.name in original_winners:
            results[p.name]['winner'] = 1

    STEP = 0.1  # 10%
    PRECISION = 100
    MAX_COST = get_max_cost(region, instance.budget_limit)
    print(MAX_COST)

    num_projects = len(instance)

    for r in tqdm(range(num_rounds)):
        # print(f'Round {r}')

        winners_default = compute_winners(instance, profile, method)
        # print(winners_default)

        instance_list = [p for p in instance]
        c = np.random.choice(instance_list, 1)[0]

        original_c_cost = c.cost

        if c.name in winners_default and c.cost != MAX_COST:

            # c.cost *= (1 + STEP)
            # c.cost = int(c.cost)
            increase = int(max(100, c.cost * STEP))
            c.cost += increase

            if c.cost > MAX_COST:
                c.cost = MAX_COST
                # print('upper limit')

            winners_tmp = compute_winners(instance, profile, method)

            if c.name not in winners_tmp:
                c.cost = original_c_cost
                # print('If I increase I lose')

        elif c.name not in winners_default and c.cost != 1:

            # c.cost *= (1 - STEP)
            # c.cost = int(c.cost)
            decrease = int(max(100, c.cost * STEP))
            c.cost -= decrease

            if c.cost <= 0:
                c.cost = 1
                # print('lower limit')

    for p in instance:
        results[p.name]['last_cost'] = p.cost

    _store_game_results_in_csv(region, name, method, results)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        regions = [
            # 'krakow_2020',
            # 'krakow_2021',
            # 'krakow_2022',
            'warszawa_2023'
        ]
    else:
        regions = [str(sys.argv[1])]

    for region in regions:

        for name in NAMES[region]:
            print(name)

            # compute_iterative_game(region, name, 'greedy_cost_sat')
            compute_iterative_game(region, name, 'greedy_cardinality_sat', num_rounds=400)
            # compute_winning_margins(region, name, 'phragmen')

            # compute_winning_margins(region, name, 'mes_phragmen')

            # compute_losing_margins(region, name, 'greedy_cost_sat')
            # compute_losing_margins(region, name, 'greedy_cardinality_sat')
            # compute_losing_margins(region, name, 'phragmen')

            # compute_losing_margins(region, name, 'mes_phragmen')

            # test_budgets(region, name)
            break


# [mpq(21113,1), mpq(22761,1), mpq(23185,1), mpq(23344,1), mpq(24681,1), mpq(27296,1), mpq(31082,1), mpq(33724,1), mpq(34884,1), mpq(35758,1), mpq(36028,1), mpq(36568,1), mpq(38692,1), mpq(39283,1), mpq(40585,1), mpq(40962,1), mpq(41859,1), mpq(42952,1), mpq(44897,1), mpq(45874,1), mpq(47310,1), mpq(48791,1), mpq(49222,1), mpq(49332,1), mpq(50036,1), mpq(50824,1), mpq(56388,1), mpq(66375,1), mpq(68931,1)]
