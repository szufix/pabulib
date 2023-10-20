import csv
import os
import matplotlib.pyplot as plt
from glossary import NAMES
from matplotlib.transforms import Bbox
from matplotlib.markers import MarkerStyle
import sys

import ast
from glossary import *
from _utils import *

from scipy import stats

from sklearn.manifold import MDS
import numpy as np
# import mapel.elections as mapel
from PIL import Image
import math
#
from pabutools.rules import equal_shares, utilitarian_greedy
from pabutools.model import Election

plt.rcParams["font.family"] = "Times New Roman"


def get_max_cost(region, budget):
    if region in ['krakow_2020', 'krakow_2021', 'krakow_2022']:
        return budget*0.4
    elif region in ['warszawa_2020', 'warszawa_2021', 'warszawa_2022', 'warszawa_2023']:
        return budget*0.2
    # print(region)


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
        new_winners.add(w.idx)
    return new_winners


def verify_cost(winners):
    total = 0
    for w in winners:
        total += w.cost
    print(total)


def _store_results_in_csv(region, name, method, A, B, C, type):
    name = name.replace('.pb','')
    path = os.path.join(os.getcwd(), "margins", type, region, f'{name}_{method}.csv')
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["idx", "cost", "max_cost", "ratio", "difference"])
        for i in range(len(A)):
        #     print(A[i], B[i], C[i])
        #     print(A[i], B[i], C[i], C[i] / B[i], C[i] - B[i])
            writer.writerow([A[i], B[i], C[i], C[i] / B[i], C[i] - B[i]])


# def get_winners(election, method):
#     if method == 'mes':
#         winners_tmp = equal_shares(election, completion='add1_utilitarian')
#         winners_tmp = convert_winners(winners_tmp)
#     elif method == 'greedy':
#         winners_tmp = utilitarian_greedy(election)
#         winners_tmp = convert_winners(winners_tmp)
#     return winners_tmp


def compute_winning_margins(region, name, method):
    A = []
    B = []
    C = []

    election = import_election(region, name)

    winners_default = compute_winners(election, method)

    PRECISION = 100
    MAX_COST = get_max_cost(region, election.budget)

    for c in election.profile:

        if c.idx in winners_default:

            original_c_cost = c.cost

            left = c.cost
            right = MAX_COST

            while right - left > PRECISION:

                c.cost = int(left + (right - left) / 2)

                winners_tmp = compute_winners(election, method)

                if c.idx in winners_tmp:
                    left = c.cost
                else:
                    right = c.cost

            A.append(c.idx)
            B.append(original_c_cost)
            C.append(c.cost)

            c.cost = original_c_cost

    _store_results_in_csv(region, name, method, A, B, C, 'winning')


def compute_losing_margins(region, name, method):
    A = []
    B = []
    C = []

    election = import_election(region, name)
    winners_default = compute_winners(election, method)

    PRECISION = 100
    MIN_COST = 100

    for c in election.profile:

        if c.idx not in winners_default:

            original_c_cost = c.cost

            left = MIN_COST
            right = c.cost

            while right - left > PRECISION:

                c.cost = int(left + (right - left) / 2)

                winners_tmp = compute_winners(election, method)

                if c.idx in winners_tmp:
                    left = c.cost
                else:
                    right = c.cost

            A.append(c.idx)
            B.append(original_c_cost)
            C.append(c.cost)

            c.cost = original_c_cost

    _store_results_in_csv(region, name, method, A, B, C, 'losing')


def test_budgets(region, name):

    path = f"data/{region}/{name}"

    election = Election()
    election.read_from_files(path)

    budget = election.budget
    sum_costs = sum([c.cost for c in election.profile])
    ratio = round(sum_costs / budget, 2)
    print(f'{budget}, {sum_costs}, {ratio}')


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
            compute_winning_margins(region, name, 'greedy')
            # compute_winning_margins(region, name, 'mes')
            compute_losing_margins(region, name, 'greedy')
            # compute_losing_margins(region, name, 'mes')
            # test_budgets(region, name)
            break

