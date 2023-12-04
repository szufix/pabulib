

import matplotlib.pyplot as plt

from glossary import NAMES


import csv

def import_pb(path):
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        meta = {}
        projects = {}
        votes = {}
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
    return projects, votes, meta


def print_czestochowa(year):

    projects, votes, meta = import_pb(f"pabulib_877/poland_czestochowa_{year}_.pb")

    tens = 0
    fives = 0
    ones = 0
    for values in votes.values():
        # print(values['points'])
        if values['points'] == "10":
            tens += 1
        elif values['points'] == "5,5":
            fives += 1
        elif values['points'] == "1":
            ones += 1

    print(tens/len(votes), fives/len(votes), ones/len(votes))

    incomplete = 0
    for values in votes.values():
        points = values['points'].split(",")
        total = sum([int(p) for p in points])
        if total < 10:
            incomplete += 1
            print(points)

    print(incomplete/len(votes))


def print_katowice(year):

    projects, votes, meta = import_pb(f"pabulib_877/poland_katowice_{year}_.pb")

    threes = 0
    ones = 0
    for values in votes.values():
        # print(values['points'])
        if values['points'] == "3":
            threes += 1
        elif values['points'] == "1":
            ones += 1

    print(threes/len(votes), ones/len(votes))

    incomplete = 0
    for values in votes.values():
        points = values['points'].split(",")
        total = sum([int(p) for p in points])
        if total < 3:
            incomplete += 1

    print(incomplete/len(votes))


def print_gdansk(year):
    for name in NAMES[f'gdansk_{year}']:
        print(name)
        projects, votes, meta = import_pb(f"pabulib_877/{name}")

        fives = 0
        ones = 0
        for values in votes.values():
            # print(values['points'])
            if values['points'] == "5":
                fives += 1
            elif values['points'] == "1":
                ones += 1

        print(fives / len(votes), ones / len(votes))

        incomplete = 0
        in_M = 0
        in_F = 0
        all_M = 0
        all_F = 0
        in_Age = []
        all_Age = []
        for values in votes.values():
            points = values['points'].split(",")
            total = sum([int(p) for p in points])
            if values['sex'] == 'M':
                all_M += 1
            elif values['sex'] == 'F':
                all_F += 1

            if total < 5:
                incomplete += 1
                if values['sex'] == 'M':
                    in_M += 1
                elif values['sex'] == 'F':
                    in_F += 1
                in_Age.append(int(values['age']))
        all_Age = [int(values['age']) for values in votes.values()]

        print(incomplete / len(votes))
        print(in_M, all_M, in_F, all_F)
        print(in_M / all_M, in_F / all_F)
        print(sum(in_Age)/len(in_Age), sum(all_Age)/len(all_Age))


if __name__ == "__main__":

    year = 2020
    print_gdansk(year)
