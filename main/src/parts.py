import itertools

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import stats

import mapel.elections as mapel

import os
import csv

from mapel.core.matchings import solve_matching_vectors

from .rules import *


## PARTS

def convert_pabulib_data(experiment_id):
    directory =  os.path.join(os.getcwd(), "experiments", experiment_id, 'rules_input', 'elections')
    # List all files in the given directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Sort the files for consistency
    files.sort()

    # Rename each file
    for idx, file_name in enumerate(files, start=1):
        # Create the new file name
        new_file_name = f"pabulib_{idx}{os.path.splitext(file_name)[1]}"

        # Form the full old and new paths
        old_path = os.path.join(directory, file_name)
        new_path = os.path.join(directory, new_file_name)

        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed {file_name} -> {new_file_name}")



def export_committees_to_file(experiment_id, rule_name, all_winning_committees):
    path = os.path.join(os.getcwd(), "experiments", experiment_id, 'rules_input', 'features',
                        f'{rule_name}.csv')
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["election_id", "committee"])
        for election_id in all_winning_committees:
            writer.writerow([election_id, [set(all_winning_committees[election_id])]])


from pabutools.election import parse_pabulib


def import_pabulib_election(experiment_id, name_pb):
    path = f'experiments/{experiment_id}/rules_input/elections/{name_pb}'
    instance, profile = parse_pabulib(path)
    return instance, profile


def compute_rules(experiment_id, size, MAIN_RULE_IDS):
    for rule in MAIN_RULE_IDS:
        print(rule)
        results = {}

        for i in range(size):
            name_pb = f'pabulib_{i}.pb'
            instance, profile = import_pabulib_election(experiment_id, name_pb)

            winners_default = compute_winners(instance, profile, rule)

            name = name_pb.replace('.pb', '')
            results[name] = winners_default

        export_committees_to_file(experiment_id, rule, results)
