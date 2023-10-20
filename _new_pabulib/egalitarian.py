import csv
import os
import matplotlib.pyplot as plt
from glossary import NAMES
from matplotlib.transforms import Bbox
from matplotlib.markers import MarkerStyle
import sys

import ast

from scipy import stats

from sklearn.manifold import MDS
import numpy as np
from PIL import Image
import math

from _utils import *
from ilp import egalitarian_ilp


def get_ideal_spending(region, name):
    path = f"data/{region}/{name}"
    meta, projects, votes = import_data(path)

    return [float(meta['budget']) / len(votes) for _ in range(len(votes))]


def diff(x, y):
    if x > y:
        return (1. - y/x)**2
    return 0


def compute_egalitarian_measure(region, name, method):
    path = f"data/{region}/{name}"
    winners = get_winners(path, method)
    meta, projects, votes = import_data(path)

    # move to utils
    acs = {project_id: set() for project_id in projects}

    for vote_id in votes:
        vote = ast.literal_eval(votes[vote_id]['vote'])
        if type(vote) == int:
            vote = [vote]
        for project_id in vote:
            acs[str(project_id)].add(str(vote_id))
    # end
    spending = {vote_id: 0. for vote_id in votes}
    for project_id in winners:
        share = float(projects[project_id]['cost']) / len(acs[project_id])
        for vote_id in acs[project_id]:
            spending[vote_id] += share

    return sorted(spending.values(), reverse=True)


if __name__ == "__main__":

    instance_type = 'approval'
    distance_id = 'jaccard'

    if len(sys.argv) < 2:
        regions = [
            'snochaczewo',
        ]
    else:
        regions = [str(sys.argv[1])]

    for region in regions:

        for name in NAMES[region]:
            print(name)

            path = f"data/{region}/{name}"
            meta, projects, votes = import_data(path)
            budget = int(meta['budget'])
            num_projects = len(projects)

            acs = {project_id: set() for project_id in projects}
            for vote_id in votes:
                vote = ast.literal_eval(votes[vote_id]['vote'])
                if type(vote) == int:
                    vote = [vote]
                for project_id in vote:
                    acs[str(project_id)].add(str(vote_id))
            x = egalitarian_ilp(votes, projects, budget, num_projects, acs)
            print(x)
            # spending_greedy = compute_egalitarian_measure(region, name, 'greedy')
            # spending_mes = compute_egalitarian_measure(region, name, 'mes')
            # spending_equal = compute_egalitarian_measure(region, name, 'equal')
            # spending_ideal = get_ideal_spending(region, name)
            #
            # plt.plot(spending_greedy, color='red', alpha=0.75)
            # plt.plot(spending_mes, color='blue', alpha=0.75)
            # plt.plot(spending_equal, color='purple', alpha=0.75)
            # plt.plot(spending_ideal, color='green', alpha=0.75)
            # nice_name = name.replace('.pb', '')
            # plt.savefig(f'images/egalitarian/{nice_name}', dpi=200, bbox_inches='tight')
            # # plt.show()
            # plt.clf()
            #
            # greedy_diff = round(sum(diff(x,y) for x, y in zip(spending_ideal, spending_greedy)), 2) \
            #               / len(spending_ideal)
            # mes_diff = round(sum(diff(x,y) for x, y in zip(spending_ideal, spending_mes)), 2) \
            #            / len(spending_ideal)
            # print(greedy_diff, mes_diff)