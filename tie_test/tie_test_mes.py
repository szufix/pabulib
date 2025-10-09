import os
from pabutools.election import Cost_Sat, Cardinality_Sat
from pabutools.election import parse_pabulib
from pabutools.rules import completion_by_rule_combination
from pabutools.rules import exhaustion_by_budget_increase
from pabutools.rules import greedy_utilitarian_welfare, method_of_equal_shares, sequential_phragmen

from pabutools.tiebreaking import refuse_tie_breaking
from tqdm import tqdm

def import_election(name):
    path = f'data_705/{name}'
    instance, profile = parse_pabulib(path)
    return instance, profile


def get_all_file_names():
    path = f'data_705'
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # Sort the files for consistency
    files.sort()
    return files

# import refuse_tie_breaking



file_names = get_all_file_names()

num_of_ties = 0
for name in tqdm(file_names):
    instance, profile = import_election(name)

    # compute winners
    winners_default = completion_by_rule_combination(
        instance,
        profile,
        [method_of_equal_shares, sequential_phragmen],
        [
            {"sat_class": Cost_Sat}, {}
        ],
        resoluteness=False,
    )
    if len(winners_default) > 1:
        num_of_ties += 1
        print(name)

print(len(file_names))
print(num_of_ties)
print(num_of_ties/len(file_names))

