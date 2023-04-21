import sys
from glossary import *
from _utils import *
import itertools
import copy
import os

from pabutools.model import Election, Candidate


def bundling(election, c1, c2):
    new_election = copy.deepcopy(election)

    new_c = Candidate(id='bundle', cost=c1.cost+c2.cost, name='bundle')
    new_election.profile[new_c] = election.profile[c1] | election.profile[c2]

    del new_election.profile[c1]
    del new_election.profile[c2]

    return new_election, new_c


def main_experiment(region, name, method):

    election = import_election(region, name)
    winners = compute_winners(election, method)
    print(winners)

    for c in election.profile:
        print(c, len(election.profile[c].values()))

    results = {
        'win, both win': 0,
        'win, single win': 0,
        'win, both lose': 0,
        'lose, both win': 0,
        'lose, single win': 0,
        'lose, both lose': 0,
    }

    for c1, c2 in itertools.combinations(election.profile, r=2):

        new_election, new_c = bundling(election, c1, c2)
        new_winners = compute_winners(new_election, method)

        if new_c.id in new_winners:
            if c1.id in winners and c2.id in winners:
                results['win, both win'] += 1
            elif c1.id in winners or c2.id in winners:
                results['win, single win'] += 1
            else:
                results['win, both lose'] += 1
        else:
            if c1.id in winners and c2.id in winners:
                print(c1.id, c2.id)
                results['lose, both win'] += 1
            elif c1.id in winners or c2.id in winners:
                results['lose, single win'] += 1
            else:
                results['lose, both lose'] += 1

    return results


if __name__ == "__main__":

    if len(sys.argv) < 2:
        regions = [
            'warszawa_2021',
        ]
    else:
        regions = [str(sys.argv[1])]

    for region in regions:

        for name in NAMES[region]:

            results_greedy = main_experiment(region, name, 'greedy')
            results_mes = main_experiment(region, name, 'mes')

            # store in csv file
            name = name.replace('.pb', '')
            path = os.path.join(os.getcwd(), "bundling", region, f'{name}.csv')
            with open(path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(['win, both win',
                                'win, single win',
                                'win, both lose',
                                'lose, both win',
                                'lose, single win',
                                'lose, both lose'])
                writer.writerow([results_greedy['win, both win'],
                                results_greedy['win, single win'],
                                results_greedy['win, both lose'],
                                results_greedy['lose, both win'],
                                results_greedy['lose, single win'],
                                results_greedy['lose, both lose']])
                writer.writerow([results_mes['win, both win'],
                                results_mes['win, single win'],
                                results_mes['win, both lose'],
                                results_mes['lose, both win'],
                                results_mes['lose, single win'],
                                results_mes['lose, both lose']])