from src.distances import *
from src.parts import *

MAIN_RULE_IDS = [
    'greedy_cost_sat',
    'greedy_card_sat',
    'max_cost_sat',
    'max_card_sat',
    'phragmen',
    'mes_cost_phragmen',
    ### 'mes_cost_epsilon': mes_cost_epsilon,
    ###'mes_cost_add1u',
    'mes_card_phragmen',
    ### 'mes_card_epsilon': mes_card_epsilon,
    ### 'mes_card_add1u',
    'mtc',
    'ewtc',
    'mt',
    'ewt',
    ### 'pav': compute_pav,
]


def convert_committee(instance, com):
    new_com = []
    for c in instance:
        if int(c.name) in com:
            new_com.append(c)
    return new_com


if __name__ == "__main__":

    parts = [2,3,4,5]

    size = 19
    distance_id = 'discrete'
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

            with open(path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(["election_id_1", "election_id_2", "distance", "time"])

                for i, r1 in enumerate(list_of_rules):
                    for j, r2 in enumerate(list_of_rules):
                        if i < j:

                            all_distance = []
                            for idx, election_id in enumerate(experiment.elections):

                                com1 = experiment.all_winning_committees[r1][
                                    election_id][0]
                                com2 = experiment.all_winning_committees[r2][
                                    election_id][0]

                                name_pb = f'pabulib_{idx}.pb'
                                instance, profile = import_pabulib_election(experiment_id, name_pb)

                                com1 = convert_committee(instance, com1)
                                com2 = convert_committee(instance, com2)

                                if distance_id == 'discrete':
                                    distance = compute_flow_distance(instance, profile, com1, com2)

                                all_distance.append(distance)

                            mean = sum(all_distance) / experiment.num_elections
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
                textual=MAIN_RULE_IDS,
                saveas='test_1',
                legend=False,
                textual_size=8)
