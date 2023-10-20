import csv
import matplotlib.pyplot as plt
import ast
from scipy.stats import stats
import math

import os

def vote_length_vs_sex(votes, projects):
    men = []
    women = []
    women_costs = []
    men_costs = []
    for vote_id in votes:
        vote = votes[vote_id]['vote']
        if ',' in vote:
            vote = ast.literal_eval(vote)
        else:
            vote = [vote]

        vote_length = len(vote)

        cost = 0
        for project in vote:
            # print(vote)
            cost += float(projects[str(project)]['cost'])

        value = votes[vote_id]['sex']
        if value == 'F':
            women.append(vote_length)
            women_costs.append(cost)
        elif value == 'M':
            men.append(vote_length)
            men_costs.append(cost)

    # print('           cost woman: ', sum(women_costs)/len(women_costs) / (sum(women)/len(women)), len(women_costs))
    # print('             cost man: ', sum(men_costs)/len(men_costs) / (sum(men)/len(men)), len(men_costs))
    # print('avg vote length woman: ', sum(women)/len(women), len(women))
    # print('avg vote length man:   ', sum(men)/len(men), len(men))
    a = (sum(women)/len(women))
    b = (sum(men)/len(men))
    # print( a / b,  len(women)/len(men) )

    return  a / b, len(women)/len(men)


def import_data(path):
    meta = {}
    projects = {}
    votes = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        section = ""
        header = []
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if str(row[0]).strip().lower() in ["meta", "projects", "votes"]:
                section = str(row[0]).strip().lower()
                header = next(reader)
            elif section == "meta":
                meta[row[0]] = row[1].strip()
            elif section == "projects":
                projects[row[0]] = {}
                for it, key in enumerate(header[1:]):
                    projects[row[0]][key.strip()] = row[it+1].strip()
            elif section == "votes":
                votes[row[0]] = {}
                for it, key in enumerate(header[1:]):
                    votes[row[0]][key.strip()] = row[it+1].strip()
    return meta, projects, votes


if __name__ == "__main__":

    # NAMES = {
    #     'poland_warszawa_2022_.pb',
    #     'poland_warszawa_2022_bemowo.pb',
    #     'poland_warszawa_2022_bialoleka.pb',
    #     'poland_warszawa_2022_bielany.pb',
    #     'poland_warszawa_2022_mokotow.pb',
    #     'poland_warszawa_2022_ochota.pb',
    #     'poland_warszawa_2022_praga-polnoc.pb',
    #     'poland_warszawa_2022_praga-poludnie.pb',
    #     'poland_warszawa_2022_rembertow.pb',
    #     'poland_warszawa_2022_srodmiescie.pb',
    #     'poland_warszawa_2022_targowek.pb',
    #     'poland_warszawa_2022_ursus.pb',
    #     'poland_warszawa_2022_ursynow.pb',
    #     'poland_warszawa_2022_wawer.pb',
    #     'poland_warszawa_2022_wesola.pb',
    #     'poland_warszawa_2022_wilanow.pb',
    #     'poland_warszawa_2022_wlochy.pb',
    #     'poland_warszawa_2022_wola.pb',
    #     'poland_warszawa_2022_zoliborz.pb'}

    # assign directory

    DIR_LIST = {
        # 'data/warszawa_2020',
        #         'data/warszawa_2021',
        #         'data/warszawa_2022',
        'data/wroclaw_2020'
                }

    for directory in DIR_LIST:

        test_1 = []
        test_2 = []

        # iterate over files in
        # that directory
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                # print(f)

                meta, projects, votes = import_data(f)

                x, y = vote_length_vs_sex(votes, projects)
                # print(x, y)
                test_1.append(x)
                test_2.append(y)

        print("---")
        print("vote length woman / vote length man", round(sum(test_1)/len(test_1), 3))
        print("woman / man", round(sum(test_2)/len(test_2), 3))


