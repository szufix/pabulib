import csv
import matplotlib.pyplot as plt
import ast
from scipy.stats import stats
import math


def cost_vs_support_correlation(projects):

    X = []
    Y = []
    for project in projects.values():
        X.append(float(project['cost']))
        Y.append(float(project['votes']))

    plt.scatter(X, Y)
    plt.show()

    print(round(stats.pearsonr(X, Y)[0], 4))


def vote_type_vs_sex_correlation(votes):
    X = []
    Y = []
    for vote_id in votes:
        vote_type = votes[vote_id]['voting_method']
        if vote_type == 'paper':
            vote_type = 0
        elif vote_type == 'internet':
            vote_type = 1


        value = votes[vote_id]['sex']
        if value == 'F':
            value = 0
        elif value == 'M':
            value = 1
        # value = votes[vote_id]['age']
        # value = int(value)

        X.append(value)
        Y.append(vote_type)

    print(round(stats.pearsonr(X, Y)[0], 4))


def vote_type_vs_age_correlation(votes):
    X = []
    Y = []
    for vote_id in votes:
        vote_type = votes[vote_id]['voting_method']
        if vote_type == 'paper':
            vote_type = 0
        elif vote_type == 'internet':
            vote_type = 1


        # value = votes[vote_id]['sex']
        # if value == 'F':
        #     value = 0
        # elif value == 'M':
        #     value = 1
        value = votes[vote_id]['age']
        value = int(value)

        X.append(value)
        Y.append(vote_type)

    # print(max(X))
    #
    # plt.scatter(X, Y)
    # plt.show()

    print(round(stats.pearsonr(X, Y)[0], 4))



def _voters_correlation(votes, column_id='age'):
    X = []
    Y = []
    men = []
    women = []
    for vote_id in votes:
        vote = votes[vote_id]['vote']
        vote_length = 1
        if ',' in vote:
            vote_length = len(ast.literal_eval(vote))

        value = votes[vote_id][column_id]
        if column_id == 'age':
            value = int(value)
        elif column_id == 'sex':
            if value == 'F':
                value = 0
                women.append(vote_length)
            elif value == 'M':
                value = 1
                men.append(vote_length)


        X.append(value)
        Y.append(vote_length)

    if column_id=='sex':
        print('avg vote length woman: ', sum(women)/len(women))
        print('avg vote length man:   ', sum(men)/len(men))

    print(round(stats.pearsonr(X, Y)[0], 4))


def vote_length_vs_age_correlation(votes):
    return _voters_correlation(votes, column_id='age')


def vote_length_vs_sex_correlation(votes):
    return _voters_correlation(votes, column_id='sex')



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

    # for i in range(22):
    # path = f"data/pabulib_{i}.pb"
    NAMES = {
    'poland_warszawa_2022_.pb',
    'poland_warszawa_2022_bemowo.pb',
    'poland_warszawa_2022_bialoleka.pb',
    'poland_warszawa_2022_bielany.pb',
    'poland_warszawa_2022_mokotow.pb',
    'poland_warszawa_2022_ochota.pb',
    'poland_warszawa_2022_praga-polnoc.pb',
    'poland_warszawa_2022_praga-poludnie.pb',
    'poland_warszawa_2022_rembertow.pb',
    'poland_warszawa_2022_srodmiescie.pb',
    'poland_warszawa_2022_targowek.pb',
    'poland_warszawa_2022_ursus.pb',
    'poland_warszawa_2022_ursynow.pb',
    'poland_warszawa_2022_wawer.pb',
    'poland_warszawa_2022_wesola.pb',
    'poland_warszawa_2022_wilanow.pb',
    'poland_warszawa_2022_wlochy.pb',
    'poland_warszawa_2022_wola.pb',
    'poland_warszawa_2022_zoliborz.pb'}

    NAMES = {
        'wroclaw_2020/poland_wroclaw_2020_.pb'
    }

    for name in NAMES:
        path = f"data/{name}"
        print(path)
        meta, projects, votes = import_data(path)

        vote_length_vs_age_correlation(votes)
        vote_length_vs_sex_correlation(votes)

        cost_vs_support_correlation(projects)

        vote_type_vs_age_correlation(votes)
        vote_type_vs_sex_correlation(votes)



