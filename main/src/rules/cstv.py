import math
import numpy as np
import os

from collections.abc import Iterable
from copy import deepcopy
from numbers import Number

from pabutools.fractions import frac
from pabutools.election.profile import AbstractProfile
from pabutools.election import (
    Instance,
    Project,
    total_cost,
    ApprovalProfile,
    ApprovalMultiProfile,
    AbstractApprovalBallot,
    AbstractApprovalProfile,
)
from pabutools.tiebreaking import TieBreakingRule, lexico_tie_breaking

INFTY = math.inf


# HELPER FUNCTIONS
def _buy_with_surplus(votes, num_voters, max_ratio, max_id, surplus):
    for v in range(num_voters):

        if max_id in votes[v] and votes[v][str(max_id)] != 0:

            local_surplus = votes[v][max_id] * (1. - 1. / max_ratio)
            coins_left = 0.
            votes[v][max_id] = 0.

            for key in votes[v]:
                coins_left += votes[v][key]

            if coins_left > 0.:
                surplus_ratio = (local_surplus + coins_left) / coins_left
                for key in votes[v]:
                    votes[v][key] *= surplus_ratio

            elif coins_left == 0.:
                surplus += local_surplus

    return votes, surplus


def _buy_from_transfers(votes, num_voters, max_ratio, max_id, cost):
    still_needed = cost * (1. - max_ratio)
    shares = compute_shares(votes, num_voters, max_id, still_needed)

    for v in range(num_voters):

        votes[v][max_id] = 0.

        sum_ = 0.
        for key in votes[v]:
            sum_ += votes[v][key]

        coins_left = sum_ - votes[v][max_id]

        if coins_left > 0.:
            deficit_ratio = (coins_left - shares[v]) / coins_left
            for key in votes[v]:
                if votes[v][key] != 0.:
                    votes[v][key] *= deficit_ratio

    return votes


def compute_shares(votes, num_voters, max_id, still_needed):
    shares = [0. for _ in range(num_voters)]
    money_left = [0. for _ in range(num_voters)]
    money_to_pay = [0. for _ in range(num_voters)]

    for v in range(num_voters):

        sum_ = 0.
        for key in votes[v]:
            sum_ += votes[v][key]

        poco = 0.
        if max_id in votes[v]:
            poco = votes[v][max_id]

        money_left[v] = sum_ - poco

    while still_needed > 0.1:

        current_support = 0.
        for v in range(num_voters):
            if max_id in votes[v] and money_left[v] > 0.:
                current_support += votes[v][max_id]

        if current_support < 0.01:
            break

        for v in range(num_voters):

            if max_id in votes[v]:
                money_to_pay[v] = (votes[v][max_id] / current_support) * still_needed

            if money_to_pay[v] < money_left[v]:
                still_needed -= money_to_pay[v]
                shares[v] += money_to_pay[v]
                money_left[v] -= money_to_pay[v]
            else:
                still_needed -= money_left[v]
                shares[v] += money_left[v]
                money_left[v] = 0.

    return shares


def eliminate_with_transfers(votes, min_id, surplus):
    for v in range(len(votes)):

        if min_id in votes[v] and votes[v][min_id] > 0.:

            local_surplus = votes[v][min_id]
            coins_left = 0.
            votes[v][min_id] = 0.

            for key in votes[v]:
                coins_left += votes[v][key]
            if coins_left > 0.:
                surplus_ratio = (local_surplus + coins_left) / coins_left
                for key in votes[v]:
                    votes[v][key] *= surplus_ratio
            elif coins_left == 0.:
                surplus += local_surplus

    return votes, surplus


def cheapest_project_left(costs, winners):
    cheapest = INFTY
    for key in costs:
        if key not in winners and costs[key] < cheapest:
            cheapest = costs[key]

    return cheapest


def remove_expensive(votes, costs, num_projects, num_voters, budget):
    ratio = {}
    for i in range(len(votes)):
        for key in votes[i]:
            if key in ratio:
                ratio[key] += votes[i][key]
            else:
                ratio[key] = votes[i][key]

    too_expensive = 0.

    for p in costs:
        if costs[p] >= budget:

            too_expensive += ratio[p]
            for v in range(num_voters):
                votes[v][p] = 0.

    total = 0.
    for i in range(len(votes)):
        for key in votes[i]:
            total += votes[i][key]

    if total == 0.:
        for p in range(num_projects):
            for v in range(num_voters):
                votes[v][p] = 0.
    else:
        defl = (total + too_expensive) / total

        for i in range(len(votes)):
            for key in votes[i]:
                votes[i][key] *= defl
    return votes


def deflation(votes, surplus):
    total = 0.
    for i in range(len(votes)):
        for key in votes[i]:
            total += votes[i][key]

    defl = (total + float(surplus)) / total

    for i in range(len(votes)):
        for key in votes[i]:
            votes[i][key] *= defl

    return votes


def prepare_votes(votes, budget):
    num_coins = 0.
    for i in range(len(votes)):
        for key in votes[i]:
            num_coins += votes[i][key]

    coin_value = budget / num_coins

    for i in range(len(votes)):
        for key in votes[i]:
            votes[i][key] *= coin_value

    return votes


# convert
def get_weighted_votes_from_profile(profile):
    num_voters = len(profile)
    weighted_votes = [{} for _ in range(num_voters)]
    for i, vote in enumerate(profile):
        for c in vote:
            weighted_votes[i][c] = 1
    return weighted_votes



# PRINCIPAL METHODS
def compute_MTC(instance: Instance, profile: AbstractProfile):

    budget = instance.budget_limit

    votes = get_weighted_votes_from_profile(profile)
    votes = prepare_votes(votes, budget)

    costs = {project: project.cost for project in instance}

    num_votes = len(votes)

    winners = []
    is_ending = False

    while True:
        ratio = {}
        for i in range(num_votes):
            for key in votes[i]:
                if key in ratio:
                    ratio[key] += votes[i][key]
                else:
                    ratio[key] = votes[i][key]

        max_ratio = 0.
        max_id = 0
        surplus = 0.

        for key in ratio:
            ratio[key] /= costs[key]
            if ratio[key] > max_ratio:
                max_ratio = ratio[key]
                max_id = key

        if not is_ending:

            if max_ratio >= 1:

                winners.append(max_id)
                budget -= costs[max_id]
                votes, surplus = _buy_with_surplus(votes, num_votes, max_ratio, max_id, surplus)

            else:
                max_ratio = 0.
                max_id = -1

                for key in costs:

                    money = 0
                    for v in range(num_votes):
                        if key in votes[v] and votes[v][key] > 0.:
                            for p in votes[v]:
                                money += votes[v][p]

                    if money >= costs[key]:

                        if ratio[key] > max_ratio:
                            max_ratio = ratio[key]
                            max_id = key

                if max_id == -1:
                    is_ending = True
                else:
                    winners.append(max_id)
                    budget -= costs[max_id]

                    for v in range(num_votes):
                        if max_id in votes[v] and votes[v][max_id] > 0.:
                            for p in votes[v]:
                                money += votes[v][p]

                    votes = _buy_from_transfers(votes, num_votes, max_ratio, max_id, costs[max_id])

        else:

            max_ratio = -INFTY
            max_id = -1

            for w in ratio:
                if budget >= costs[w] and w not in winners:
                    if ratio[w] > max_ratio:
                        max_ratio = ratio[w]
                        max_id = w

            if max_id == -1:
                break
            else:
                winners.append(max_id)
                budget -= costs[max_id]
                for v in range(num_votes):
                    votes[v][max_id] = 0.

        if budget < cheapest_project_left(costs, winners):
            break

    return winners


def compute_EwTC(instance: Instance, profile: AbstractProfile):

    budget = instance.budget_limit

    votes = get_weighted_votes_from_profile(profile)
    votes = prepare_votes(votes, budget)

    costs = {project: project.cost for project in instance}

    num_votes = len(votes)
    num_projects = len(costs)

    winners = []
    is_ending = False

    while True:
        ratio = {}
        for i in range(num_votes):
            for key in votes[i]:
                if key in ratio:
                    ratio[key] += votes[i][key]
                else:
                    ratio[key] = votes[i][key]

        max_ratio = 0.
        max_id = 0
        surplus = 0.

        for i in ratio:
            ratio[i] /= costs[i]
            if ratio[i] > max_ratio:
                max_ratio = ratio[i]
                max_id = i

        if not is_ending:

            if max_ratio >= 1:

                winners.append(max_id)
                budget -= costs[max_id]
                votes, surplus = _buy_with_surplus(votes, num_votes, max_ratio, max_id, surplus)

            else:
                max_ratio = 0.
                max_id = -1

                for w in range(num_projects):

                    money = 0
                    for v in range(num_votes):
                        if w in votes[v] and votes[v][w] > 0.:
                            for p in votes[v]:
                                money += votes[v][p]

                    if w in votes[v] and money >= costs[w]:

                        if ratio[w] > max_ratio:
                            max_ratio = ratio[w]
                            max_id = w

                if max_id == -1:
                    is_ending = True
                else:
                    winners.append(max_id)
                    budget -= costs[max_id]

                    for v in range(num_votes):
                        if votes[v][max_id] > 0.:
                            for p in range(num_projects):
                                money += votes[v][p]

                    votes = _buy_from_transfers(votes, num_votes, max_ratio, max_id, costs[max_id])

        else:

            max_ratio = -INFTY
            max_id = -1

            for w in ratio:
                if budget >= costs[w] and w not in winners:
                    if ratio[w] > max_ratio:
                        max_ratio = ratio[w]
                        max_id = w

            if max_id == -1:
                break
            else:
                winners.append(max_id)
                budget -= costs[max_id]
                for v in range(num_votes):
                    votes[v][max_id] = 0.

        if budget < cheapest_project_left(costs, winners):
            break

    return winners


def compute_EwT(instance: Instance, profile: AbstractProfile):

    budget = instance.budget_limit

    votes = get_weighted_votes_from_profile(profile)
    votes = prepare_votes(votes, budget)

    costs = {project: project.cost for project in instance}

    num_votes = len(votes)
    num_projects = len(costs)
    winners = []
    projects_removed = []

    while True:

        surplus = 0.
        support = {}
        for i in range(num_votes):
            for key in votes[i]:
                if key in support:
                    support[key] += votes[i][key]
                else:
                    support[key] = votes[i][key]

        excess = {}
        max_excess = -INFTY
        for i in support:
            if support[i] == 0:
                excess[i] = max_excess - 1.
            else:
                excess[i] = support[i] - costs[i]

        max_support = 0.
        max_id = 0

        for i in support:
            if excess[i] > max_excess:
                max_excess = excess[i]
                max_support = support[i]
                max_id = i

        if max_excess >= 0.:
            max_ratio = max_support / costs[max_id]

            winners.append(max_id)
            budget -= costs[max_id]
            votes, surplus = _buy_with_surplus(votes, num_votes, max_ratio, max_id, surplus)

        else:

            min_support_minus_cost = INFTY
            min_id = -1

            for i in support:
                if i not in projects_removed and i not in winners:
                    if support[i] - costs[i] < min_support_minus_cost:
                        min_support_minus_cost = support[i] - costs[i]
                        min_id = i

            if len(projects_removed) + len(winners) == num_projects:
                projects_removed.reverse()
                for id in projects_removed:
                    if id in costs.keys() and budget >= costs[id]:
                        winners.append(id)
                        budget -= costs[id]
                break

            votes, surplus = eliminate_with_transfers(votes, min_id, surplus)
            projects_removed.append(min_id)

        if budget < cheapest_project_left(costs, winners):
            break

    return winners


def compute_MT(instance: Instance, profile: AbstractProfile):

    budget = instance.budget_limit

    votes = get_weighted_votes_from_profile(profile)
    costs = {project: project.cost for project in instance}

    num_votes = len(votes)

    winners = []
    ctr = 0
    votes = prepare_votes(votes, budget)
    is_ending = False

    while True:

        ctr += 1
        support = {}
        for i in range(num_votes):
            for key in votes[i]:
                if key in support:
                    support[key] += votes[i][key]
                else:
                    support[key] = votes[i][key]

        excess = {}

        max_excess = -INFTY
        for i in support:
            if support[i] == 0:
                excess[i] = max_excess - 1.
            else:
                excess[i] = support[i] - costs[i]

        max_excess = -INFTY
        for i in support:
            if support[i] == 0:
                excess[i] = max_excess - 1.
            else:
                excess[i] = support[i] - costs[i]

        max_support = 0.
        max_id = 0
        surplus = 0.

        for i in support:
            if excess[i] > max_excess:
                max_excess = excess[i]
                max_support = support[i]
                max_id = i

        if not is_ending:

            if max_excess >= 0.:
                max_ratio = max_support / costs[max_id]

                winners.append(max_id)
                budget -= costs[max_id]
                votes, surplus = _buy_with_surplus(votes, num_votes, max_ratio, max_id, surplus)

            else:

                max_support = 0.
                max_excess = -INFTY
                max_id = -1

                for w in costs:
                    money = 0
                    for v in range(num_votes):
                        if w in votes[v] and votes[v][w] > 0.:
                            for p in votes[v]:
                                money += votes[v][p]

                    if money >= costs[w]:
                        if excess[w] > max_excess:
                            max_excess = excess[w]
                            max_support = support[w]
                            max_id = w

                if max_id == -1:
                    is_ending = True
                else:

                    max_ratio = max_support / costs[max_id]
                    winners.append(max_id)
                    budget -= costs[max_id]
                    votes = _buy_from_transfers(votes, num_votes, max_ratio, max_id,
                                                costs[max_id])
        else:

            max_support = 0.
            max_excess = -INFTY
            max_id = -1

            for w in support:
                if budget >= costs[w] and w not in winners:
                    if excess[w] > max_excess:
                        max_excess = excess[w]
                        max_support = support[w]
                        max_id = w

            if max_id == -1:
                break
            else:
                max_ratio = max_support / costs[max_id]
                winners.append(max_id)
                budget -= costs[max_id]
                votes = _buy_from_transfers(votes, num_votes, max_ratio, max_id,
                                            costs[max_id])

        if budget < cheapest_project_left(costs, winners):
            break

    return winners
