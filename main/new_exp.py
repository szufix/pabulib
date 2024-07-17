import matplotlib.pyplot as plt
import numpy as np

from src.distances import *
from src.parts import *
from fractions import Fraction

MAIN_RULE_IDS = {
    'greedy_cost_sat': 'BasicAV',
    'greedy_card_sat': 'AV/cost',
    'max_cost_sat': 'Opt-BasicAV',
    'max_card_sat': 'Opt-AV/cost',
    'phragmen': 'Phragmen',
    'mes_cost_phragmen': 'MES/Ph',
    'mes_cost_epsilon': 'MES/eps',
    # 'mes_cost_add1u': 'MES/add1u',
    'mes_card_phragmen': 'MES-Apr/Ph',
    'mes_card_epsilon': 'MES-Apr/eps',
    # 'mes_card_add1u': 'MES-Apr/add1u',
    'mtc': 'MTC',
    'ewtc': 'EwTC',
    'mt': 'MT',
    'ewt': 'EwT',
    'pb_pav': 'PB-PAV',
}


if __name__ == "__main__":

    r1 = 'max_cost_sat'
    r2 = 'mt'

    experiment_id = 'pabulib'
    name_pb = f'pabulib_370.pb'

    distance_id = 'jaccard'

    instance, profile = import_pabulib_election(experiment_id, name_pb)

    budgets = list(np.linspace(100000,3000000,30))
    print(budgets)

    distances = []

    for budget in tqdm(budgets):
        instance.budget_limit = Fraction(int(budget), 1)

        w1 = compute_winners(instance, profile, r1)
        w2 = compute_winners(instance, profile, r2)

        # com1 = convert_committee(instance, com1)
        # com2 = convert_committee(instance, com2)

        distance = compute_flow_distance(instance, profile, w1, w2, distance_id)
        distances.append(distance)

    plt.ylim([0, 500000])
    plt.xlabel('Budget')
    plt.ylabel('Distance')
    plt.plot(distances)
    plt.title(f'{MAIN_RULE_IDS[r1]} vs {MAIN_RULE_IDS[r2]}')
    plt.savefig(f'{r1}_{r2}')
    plt.show()
