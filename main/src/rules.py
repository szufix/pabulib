import copy
import math
from tqdm import tqdm

from abcvoting.preferences import Profile
from abcvoting import abcrules

from pabutools.election import Cost_Sat, Cardinality_Sat
from pabutools.election import parse_pabulib

from pabutools.rules import \
    greedy_utilitarian_welfare, \
    method_of_equal_shares, \
    sequential_phragmen, \
    completion_by_rule_combination, \
    exhaustion_by_budget_increase, \
    max_additive_utilitarian_welfare, \
    social_welfare_comparison, \
    popularity_comparison


from .cstv import compute_MTC, compute_EwTC, compute_MT, compute_EwT



def compute_pav(instance, profile):
    pass


def mes_cost_phragmen(instance, profile):
    return completion_by_rule_combination(
        instance,
        profile,
        [method_of_equal_shares, sequential_phragmen],
        [
            {"sat_class": Cost_Sat}, {}
        ],
    )

def mes_cost_epsilon(instance, profile):
    pass


def mes_cost_add1u(instance, profile):
    return completion_by_rule_combination(
        instance,
        profile,
        [exhaustion_by_budget_increase, greedy_utilitarian_welfare],
        [
            {
                "rule": method_of_equal_shares,
                "rule_params": {"sat_class": Cost_Sat},
                "budget_step": instance.budget_limit / 100,
            },
            {"sat_class": Cost_Sat},
        ],
    )


def mes_card_phragmen(instance, profile):
    return completion_by_rule_combination(
        instance,
        profile,
        [method_of_equal_shares, sequential_phragmen],
        [
            {"sat_class": Cardinality_Sat}, {}
        ],
    )


def mes_card_add1u(instance, profile):
    return completion_by_rule_combination(
        instance,
        profile,
        [exhaustion_by_budget_increase, greedy_utilitarian_welfare],
        [
            {
                "rule": method_of_equal_shares,
                "rule_params": {"sat_class": Cardinality_Sat},
                "budget_step": instance.budget_limit / 100,
            },
            {"sat_class": Cardinality_Sat},
        ],
    )


def mes_card_epsilon(instance, profile):
    pass


def greedy_utilitarian_welfare_cost_sat(instance_tmp, profile_tmp):
    return greedy_utilitarian_welfare(instance_tmp, profile_tmp, sat_class=Cost_Sat)


def greedy_utilitarian_welfare_card_sat(instance_tmp, profile_tmp):
    return greedy_utilitarian_welfare(instance_tmp, profile_tmp, sat_class=Cardinality_Sat)


def max_additive_utilitarian_welfare_cost_sat(instance_tmp, profile_tmp):
    return max_additive_utilitarian_welfare(instance_tmp, profile_tmp, sat_class=Cost_Sat)


def max_additive_utilitarian_welfare_card_sat(instance_tmp, profile_tmp):
    return max_additive_utilitarian_welfare(instance_tmp, profile_tmp, sat_class=Cardinality_Sat)


registered_rules = {
    'greedy_cost_sat': greedy_utilitarian_welfare_cost_sat,
    'greedy_card_sat': greedy_utilitarian_welfare_card_sat,
    'max_cost_sat': max_additive_utilitarian_welfare_cost_sat,
    'max_card_sat': max_additive_utilitarian_welfare_card_sat,
    'phragmen': sequential_phragmen,
    'mes_cost_phragmen': mes_cost_phragmen,
    'mes_cost_epsilon': mes_cost_epsilon,
    'mes_cost_add1u': mes_cost_add1u,
    'mes_card_phragmen': mes_card_phragmen,
    'mes_card_epsilon': mes_card_epsilon,
    'mes_card_add1u': mes_card_add1u,
    'mtc': compute_MTC,
    'ewtc': compute_EwTC,
    'mt': compute_MT,
    'ewt': compute_EwT,
    'pav': compute_pav,
}

def mes_phragmen(instance, profile):
    return completion_by_rule_combination(
        instance,
        profile,
        [method_of_equal_shares, sequential_phragmen],
        [
            {"sat_class": Cost_Sat}, {}
        ],
    )


def compute_winners(instance, profile, rule):
    instance_tmp = copy.deepcopy(instance)
    profile_tmp = copy.deepcopy(profile)

    return registered_rules.get(rule)(instance_tmp, profile_tmp)

#################################################################

def convert_winners_to_set(winners):
    winners_as_set = set()
    for w in winners:
        winners_as_set.add(w.idx)
    return winners_as_set


def import_election(region, name):
    path = f'data/{region}/{name}'
    instance, profile = parse_pabulib(path)
    return instance, profile


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
            diff = {i: c.cost / len(e.profile[c]) for i in e.profile[c]}
            power_inequality = sum(
                (real_vector.get(i, 0) + diff.get(i, 0) - ideal_pt) ** 2 for i in e.voters)
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


def get_total_support(profile):
    support = 0
    for vote in profile:
        support += len(vote)
    return support


def get_supporters(profile, c):
    support = 0
    for vote in profile:
        if c.name in vote:
            support += 1
    return support


def sort_by_indexes(lst, indexes, reverse=False):
    return [val for (_, val) in sorted(zip(indexes, lst), key=lambda x: \
        x[0], reverse=reverse)]


def convert(value):
    value /= 1000
    if value > 1:
        value = round(value, 0)
        value = int(value)
    else:
        value = round(value, 1)
    return f'{value}'
