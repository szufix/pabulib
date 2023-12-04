from pabutools.election import Instance, Profile, parse_pabulib, Cost_Sat
import math


class SingleMESVoter:
        def __init__(self, sat, endow):
            self.sat = sat
            self.endow = endow

        def sat_project(self, c):
            return self.sat.sat_project(c)

        def __str__(self):
            return f"SingleMESVoter[{self.sat}]"

        def __repr__(self):
            return f"SingleMESVoter[{self.sat}]"


def method_of_equal_shares_epsilon(instance: Instance, profile: Profile, sat_class = None, sat_profile = None):
    if sat_class is None and sat_profile is None:
        raise ValueError("sat_class and sat_profile cannot both be None")
    elif sat_profile is None:
        sat_profile = profile.as_sat_profile(sat_class=sat_class)
    mes_profile = [SingleMESVoter(sat, 1.0 * instance.budget_limit / len(sat_profile)) for sat in sat_profile]
    W = set()
    costW = 0
    remaining = set(instance)
    rho = {c: c.cost / sat_profile.total_satisfaction_project(c) for c in instance}
    supporters = {c: set(v for v in mes_profile if v.sat_project(c) > 0) for c in instance}
    while True: #first loop: standard MES
        next_candidate = None
        lowest_rho = math.inf
        for c in sorted(remaining, key=lambda c: rho[c]):
            if rho[c] >= lowest_rho:
                break
            if sum(v.endow for v in supporters[c]) >= c.cost:
                supporters_sorted = sorted(supporters[c], key=lambda v: v.endow / v.sat_project(c))
                price = c.cost
                util = sat_profile.total_satisfaction_project(c)
                for v in supporters_sorted:
                    if v.endow * util >= price * v.sat_project(c):
                        break
                    price -= v.endow
                    util -= v.sat_project(c)
                rho[c] = price / util
                if rho[c] < lowest_rho:
                    next_candidate = c
                    lowest_rho = rho[c]
        if next_candidate is None:
            break
        else:
            W.add(next_candidate)
            costW += next_candidate.cost
            remaining.remove(next_candidate)
            for v in supporters[next_candidate]:
                v.endow -= min(v.endow, lowest_rho * v.sat_project(next_candidate))
    while True: #second loop: non-supporters are allowed to pay
        next_candidate = None
        lowest_rho = math.inf
        voters_sorted = sorted(mes_profile, key=lambda v: v.endow)
        for c in sorted(remaining, key=lambda c: rho[c]):
            if costW + c.cost > instance.budget_limit:
                continue
            if rho[c] >= lowest_rho:
                break
            sum_supporters = sum(v.endow for v in supporters[c])
            price = c.cost - sum_supporters
            for v in voters_sorted:
                if v not in supporters[c]:
                    continue
                if v.endow >= price:
                    rho[c] = price
                    break
                price -= v.endow
            if rho[c] < lowest_rho:
                next_candidate = c
                lowest_rho = rho[c]
        if next_candidate is None:
            break
        else:
            W.add(next_candidate)
            costW += next_candidate.cost
            remaining.remove(next_candidate)
            for v in mes_profile:
                if v in supporters[next_candidate]:
                    v.endow = 0
                else:
                    v.endow -= min(v.endow, lowest_rho)
    return W

# instance, profile = parse_pabulib("poland_krakow_2020_whole_city.pb")
# print(method_of_equal_shares_epsilon(instance, profile, sat_class=Cost_Sat))
