from fractions import Fraction
import gurobipy as gb

from pabutools.election.profile import AbstractProfile
from pabutools.election import Instance


def _pav_score(i):
    if i == 0:
        return 0
    return Fraction(1, i)


def compute_pb_pav(instance: Instance, profile: AbstractProfile):

    model = gb.Model()

    model.setParam("OutputFlag", False)
    model.setParam("PoolSearchMode", 0)
    model.setParam("MIPFocus", 2)
    model.setParam("IntegralityFocus", 1)

    all_candidates = set([p for p in instance])
    winners = model.addVars(all_candidates, vtype=gb.GRB.BINARY)

    utility = {}
    max_in_committee = {}
    for i, vote in enumerate(profile):
        max_in_committee[i] = len(vote)
        for x in range(1, max_in_committee[i] + 1):
            utility[(i, x)] = model.addVar(vtype=gb.GRB.BINARY)

    model.addConstr(sum(p.cost * winners[p] for p in instance) <= instance.budget_limit)

    for i, vote in enumerate(profile):
        model.addConstr(
            gb.quicksum(utility[(i, x)] for x in range(1, max_in_committee[i] + 1))
            == gb.quicksum(winners[p] for p in vote)
        )

    model.setObjective(
        gb.quicksum(
            float(_pav_score(x)) * utility[(i, x)]
            for i, voter in enumerate(profile)
            for x in range(1, max_in_committee[i] + 1)
        ),
        gb.GRB.MAXIMIZE,
    )

    # model.write("my_model.lp")

    model.optimize()

    committee = {cand for cand in all_candidates if winners[cand].Xn >= 0.9}
    # print(len(committee))
    return list(committee)
