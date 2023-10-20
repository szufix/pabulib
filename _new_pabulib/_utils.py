import copy
import csv
import math

from pabutools.rules import equal_shares, utilitarian_greedy
from pabutools.model import Election


def convert_winners_to_set(winners):
    winners_as_set = set()
    for w in winners:
        winners_as_set.add(w.idx)
    return winners_as_set


def compute_winners(election, method):
    election_tmp = copy.deepcopy(election)
    election_tmp.score_to_cost_utilities()
    if method == 'mes':
        winners_tmp = equal_shares(election_tmp, completion='add1_utilitarian')
        winners_tmp = convert_winners_to_set(winners_tmp)
    elif method == 'greedy':
        winners_tmp = utilitarian_greedy(election_tmp)
        winners_tmp = convert_winners_to_set(winners_tmp)
    # elif method == 'equal':
    #     winners_tmp = equal_power(election_tmp)
    #     winners_tmp = convert_winners_to_set(winners_tmp)
    else:
        winners_tmp = None
    return winners_tmp


def import_election(region, name):
    path = f'data/{region}/{name}'
    election = Election()
    election.read_from_files(path)
    return election


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


def equal_power(e):
    W = set()
    costW = 0
    ideal_pt = e.budget / len(e.voters)
    real_vector = {}
    remaining = set(e.profile.keys())
    cnt = 0
    while remaining:
        cnt += 1
        min_power_inequality = math.inf
        best_diff = None
        best_c = None
        for c in remaining:
            diff = {i : c.cost / len(e.profile[c]) for i in e.profile[c]}
            power_inequality = sum((real_vector.get(i, 0) + diff.get(i, 0) - ideal_pt) ** 2 for i in e.voters)
            if power_inequality < min_power_inequality:
                best_c = c
                best_diff = diff
                min_power_inequality = power_inequality
        W.add(best_c)
        costW += best_c.cost
        for i in best_diff:
            real_vector[i] = real_vector.get(i, 0) + best_diff[i]
        remaining.remove(best_c)
        remaining = set(c for c in remaining if c.cost + costW <= e.budget)
    return W
