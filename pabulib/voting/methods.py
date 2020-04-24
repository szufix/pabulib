import math
import numpy as np
import random as rand
import sys
import os

INFTY = 9999999.

########################

def import_data(exp_name, district):

    file_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    file_name = os.path.join(file_name, "experiments", str(exp_name), "projects", str(district) + ".txt")
    file_projects = open(file_name, 'r')

    num_projects = int(file_projects.readline())
    costs = {}

    for i in range(num_projects):
        line = file_projects.readline().replace('\n', '').split(',')
        costs[line[0]] = float(line[1])
    file_projects.close()

    file_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    file_name = os.path.join(file_name, "experiments", str(exp_name), "votes", str(district) + ".txt")
    file_votes = open(file_name, 'r')

    ballot_type = str(file_votes.readline().replace('\n', '').replace("\r", ""))
    num_votes = int(file_votes.readline())
    votes = [{} for _ in range(num_votes)]

    for i in range(num_votes):

        if ballot_type == "approval":
            line = file_votes.readline().replace('\n', '').replace("\r", "").split(',')
            for j in range(len(line)):
                votes[i][str(line[j])] = 1. / len(line)

        elif ballot_type == "cumulative":
            first_line = file_votes.readline().replace('\n', '').replace("\r", "").split(',')
            second_line = file_votes.readline().replace('\n', '').replace("\r", "").split(',')
            for j in range(len(first_line)):
                votes[i][str(first_line[j])] = float(second_line[j])

    file_votes.close()
    return votes, costs

########################

def buy_with_surplus(votes, num_voters, max_ratio, max_id, surplus):

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


def buy_from_transfers(votes, num_voters, max_ratio, max_id, cost):

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
    left = [0. for _ in range(num_voters)]
    to_pay = [0. for _ in range(num_voters)]

    for v in range(num_voters):

        sum_ = 0.
        for key in votes[v]:
            sum_ += votes[v][key]

        poco = 0.
        if max_id in votes[v]:
            poco = votes[v][max_id]

        left[v] = sum_ - poco

    while still_needed > 0.1:

        current_support = 0.
        for v in range(num_voters):
            if max_id in votes[v] and left[v] > 0.:
                current_support += votes[v][max_id]

        if current_support < 0.01:  #  possibly unnecessary
            break

        for v in range(num_voters):

            if max_id in votes[v]:
                to_pay[v] = (votes[v][max_id] / current_support) * still_needed

            if to_pay[v] < left[v]:
                still_needed -= to_pay[v]
                shares[v] += to_pay[v]
                left[v] -= to_pay[v]
            else:
                still_needed -= left[v]
                shares[v] += left[v]
                left[v] = 0.

    return shares


def cheapest_project_left(costs, winners):

    cheapest = INFTY
    for key in costs:
        if key not in winners and costs[key] < cheapest:
            cheapest = costs[key]

    return cheapest


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


########################


def save_winners_to_file(exp_name, district, method_id, winners):

    file_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    file_name = os.path.join(file_name, "experiments", str(exp_name), "winners",
                             str(district) + "_" + str(method_id) + ".txt")
    file_winners = open(file_name, 'w')
    file_winners.write(str(len(winners)) + "\n")
    for winner in winners:
        file_winners.write(str(winner) + " ")
    file_winners.write("\n")
    file_winners.close()


########################

def MTC(exp_name, district, initial_budget):
    """ Greedy by Exccess over Cost with Minimal Transfers"""
    method_id = "MTC"
    print(method_id)

    votes, costs = import_data(exp_name, district)
    num_votes = len(votes)
    winners = []
    budget = initial_budget
    votes = prepare_votes(votes, budget)
    ending = False

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

        for key in costs:
            ratio[key] /= costs[key]
            if ratio[key] > max_ratio:
                max_ratio = ratio[key]
                max_id = key

        if not ending:

            if max_ratio >= 1:

                winners.append(max_id)
                budget -= costs[max_id]
                votes, surplus = buy_with_surplus(votes, num_votes, max_ratio, max_id, surplus)

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
                    ending = True
                else:
                    winners.append(max_id)
                    budget -= costs[max_id]

                    for v in range(num_votes):
                        if max_id in votes[v] and votes[v][max_id] > 0.:
                            for p in votes[v]:
                                money += votes[v][p]

                    votes = buy_from_transfers(votes, num_votes, max_ratio, max_id, costs[max_id])
        else:

            max_ratio = -INFTY
            max_id = -1

            for w in costs:
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

    save_winners_to_file(exp_name, district, method_id, winners)

    return winners, costs

