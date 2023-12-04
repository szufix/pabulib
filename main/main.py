
import mapel.elections as mapel

from src.distances import *
from src.parts import *


MAIN_RULE_IDS = {
    ## 'mes_cost': 'MES/solo',
    ## 'mes_card': 'MES-Apr/solo',
    'greedy_cost_sat': 'BasicAV',
    'greedy_card_sat': 'AV/cost',
    'max_cost_sat': 'Opt-BasicAV',
    'max_card_sat': 'Opt-AV/cost',
    'phragmen': 'Phragmen',
    'mes_cost_phragmen': 'MES/Ph',
    'mes_cost_epsilon': 'MES/eps',
    'mes_cost_add1u': 'MES/add1u',
    'mes_card_phragmen': 'MES-Apr/Ph',
    'mes_card_epsilon': 'MES-Apr/eps',
    'mes_card_add1u': 'MES-Apr/add1u',
    'mtc': 'MTC',
    'ewtc': 'EwTC',
    'mt': 'MT',
    'ewt': 'EwT',
    'pb_pav': 'PB-PAV',
}


def convert_committee(instance, com):
    str_com = [str(c) for c in com]
    new_com = []
    for c in instance:
        if str(c.name) in str_com:
            new_com.append(c)
    return new_com


if __name__ == "__main__":

    parts = [6]

    size = 376
    distance_id = 'jaccard'
    embedding_id = 'kamada'

    names = ['pabulib']
    #
    for name in names:
        experiment_id = f'{name}'

        committee_size = 10
        list_of_rules = MAIN_RULE_IDS

        if 1 in parts:  # PREPARE ELECTIONS

            convert_pabulib_data(experiment_id)

        if 2 in parts:  # COMPUTE RULES

            compute_rules(experiment_id, size, MAIN_RULE_IDS)

        if 3 in parts:  # COMPUTE DISTANCES

            experiment = mapel.prepare_offline_approval_experiment(experiment_id=f'{experiment_id}/rules_input')

            experiment.import_committees(list_of_rules=list_of_rules)

            path = os.path.join(os.getcwd(), "experiments", f'{experiment_id}/rules_output',
                                'distances', f'{distance_id}.csv')

            instances = {}
            profiles = {}
            for idx, election_id in tqdm(enumerate(experiment.elections)):
            # for idx in range(57,58):
                name_pb = f'pabulib_{idx}.pb'
                instance, profile = import_pabulib_election(experiment_id, name_pb)
                instances[name_pb] = instance
                profiles[name_pb] = profile

            with open(path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(["election_id_1", "election_id_2", "distance", "time"])

                for i, r1 in enumerate(list_of_rules):
                    for j, r2 in enumerate(list_of_rules):
                        if i < j:
                            print(r1, r2)

                            all_distance = []
                            for idx, election_id in tqdm(enumerate(experiment.elections)):
                            # for idx in range(57, 58):
                            #     election_id = f'pabulib_{idx}'

                                com1 = experiment.all_winning_committees[r1][election_id][0]
                                com2 = experiment.all_winning_committees[r2][election_id][0]
                                name_pb = f'pabulib_{idx}.pb'

                                instance = instances[name_pb]
                                profile = profiles[name_pb]
                                com1 = convert_committee(instance, com1)
                                com2 = convert_committee(instance, com2)

                                distance = compute_flow_distance(instance, profile, com1, com2, distance_id)
                                all_distance.append(distance)

                            mean = sum(all_distance) / experiment.num_elections
                            print(mean)
                            writer.writerow([r1, r2, float(mean), 0.])

        if 4 in parts:  # EMBED

            experiment = mapel.prepare_offline_approval_experiment(experiment_id=f'{experiment_id}/rules_output',
                                                  # instance_type='rule',
                                                  distance_id=distance_id,
                                                                   fast_import=True)
            # print(election.distances)
            experiment.embed_2d(embedding_id=embedding_id)

        if 5 in parts:  # PRINT MAP

            experiment = mapel.prepare_offline_approval_experiment(experiment_id=f'{experiment_id}/rules_output',
                                                  # instance_type='rule',
                                                                   distance_id=distance_id,
                                                  embedding_id=embedding_id)

            experiment.print_map_2d(
                textual=MAIN_RULE_IDS.values(),
                saveas='test_4',
                legend=False,
                textual_size=8)

        if 6 in parts:  # PRINT MATRIX

            experiment = mapel.prepare_offline_approval_experiment(experiment_id=f'{experiment_id}/rules_output',
                                                                   distance_id=distance_id,
                                                  embedding_id=embedding_id)

            max_value = max(
                value for inner_dict in experiment.distances.values() for value in inner_dict.values())
            print(max_value)

            experiment.print_matrix(saveas=experiment_id, dpi=200, scale=1/max_value, rounding=2)

