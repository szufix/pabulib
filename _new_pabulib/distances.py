import csv
import matplotlib.pyplot as plt
import ast

from matplotlib.transforms import Bbox
from scipy import stats

from sklearn.manifold import MDS
import numpy as np
import mapel.elections as mapel
from PIL import Image
import math
from matplotlib.markers import MarkerStyle

from pabutools.rules import equal_shares, utilitarian_greedy
from pabutools.model import Election



NAMES = {}

NAMES['warszawa_2023'] = {
#     'poland_warszawa_2023_bemowo.pb': 'Bemowo',
#     'poland_warszawa_2023_bialoleka.pb': 'Białołęka',
#     'poland_warszawa_2023_bielany.pb': 'Bielany',
#     'poland_warszawa_2023_mokotow.pb': 'Mokotów',
#     'poland_warszawa_2023_ochota.pb': 'Ochota',
#     'poland_warszawa_2023_praga-polnoc.pb': 'Praga-Północ',
#     'poland_warszawa_2023_praga-poludnie.pb': 'Praga-Południe',
#     'poland_warszawa_2023_rembertow.pb': 'Rembertów',
#     'poland_warszawa_2023_srodmiescie.pb': 'Śródmieście',
    'poland_warszawa_2023_targowek.pb': 'Targówek',
    # 'poland_warszawa_2023_ursus.pb': 'Ursus',
    # 'poland_warszawa_2023_ursynow.pb': 'Ursynów',
    # 'poland_warszawa_2023_wawer.pb': 'Wawer',
    # 'poland_warszawa_2023_wesola.pb': 'Wesoła',
    # 'poland_warszawa_2023_wilanow.pb': 'Wilanów',
    # 'poland_warszawa_2023_wlochy.pb': 'Włochy',
    # 'poland_warszawa_2023_wola.pb': 'Wola',
    # 'poland_warszawa_2023_zoliborz.pb': 'Żoliborz'
}

NAMES['warszawa_2022'] = {
    'poland_warszawa_2022_bemowo.pb': 'Bemowo',
    'poland_warszawa_2022_bialoleka.pb': 'Białołęka',
    'poland_warszawa_2022_bielany.pb': 'Bielany',
    'poland_warszawa_2022_mokotow.pb': 'Mokotów',
    'poland_warszawa_2022_ochota.pb': 'Ochota',
    'poland_warszawa_2022_praga-polnoc.pb': 'Praga-Północ',
    'poland_warszawa_2022_praga-poludnie.pb': 'Praga-Południe',
    'poland_warszawa_2022_rembertow.pb': 'Rembertów',
    'poland_warszawa_2022_srodmiescie.pb': 'Śródmieście',
    'poland_warszawa_2022_targowek.pb': 'Targówek',
    'poland_warszawa_2022_ursus.pb': 'Ursus',
    'poland_warszawa_2022_ursynow.pb': 'Ursynów',
    'poland_warszawa_2022_wawer.pb': 'Wawer',
    'poland_warszawa_2022_wesola.pb': 'Wesoła',
    'poland_warszawa_2022_wilanow.pb': 'Wilanów',
    'poland_warszawa_2022_wlochy.pb': 'Włochy',
    'poland_warszawa_2022_wola.pb': 'Wola',
    'poland_warszawa_2022_zoliborz.pb': 'Żoliborz'
}

NAMES['warszawa_2021'] = {
    'poland_warszawa_2021_bemowo.pb': 'Bemowo',
    'poland_warszawa_2021_bialoleka.pb': 'Białołęka',
    'poland_warszawa_2021_bielany.pb': 'Bielany',
    'poland_warszawa_2021_mokotow.pb': 'Mokotów',
    'poland_warszawa_2021_ochota.pb': 'Ochota',
    'poland_warszawa_2021_praga-polnoc.pb': 'Praga-Północ',
    'poland_warszawa_2021_praga-poludnie.pb': 'Praga-Południe',
    'poland_warszawa_2021_rembertow.pb': 'Rembertów',
    'poland_warszawa_2021_srodmiescie.pb': 'Śródmieście',
    'poland_warszawa_2021_targowek.pb': 'Targówek',
    'poland_warszawa_2021_ursus.pb': 'Ursus',
    'poland_warszawa_2021_ursynow.pb': 'Ursynów',
    'poland_warszawa_2021_wawer.pb': 'Wawer',
    'poland_warszawa_2021_wesola.pb': 'Wesoła',
    'poland_warszawa_2021_wilanow.pb': 'Wilanów',
    'poland_warszawa_2021_wlochy.pb': 'Włochy',
    'poland_warszawa_2021_wola.pb': 'Wola',
    'poland_warszawa_2021_zoliborz.pb': 'Żoliborz'
}

NAMES['warszawa_2020'] = {
    'poland_warszawa_2020_bemowo.pb': 'Bemowo',
    'poland_warszawa_2020_bialoleka.pb': 'Białołęka',
    'poland_warszawa_2020_bielany.pb': 'Bielany',
    'poland_warszawa_2020_mokotow.pb': 'Mokotów',
    'poland_warszawa_2020_ochota.pb': 'Ochota',
    'poland_warszawa_2020_praga-polnoc.pb': 'Praga-Północ',
    'poland_warszawa_2020_praga-poludnie.pb': 'Praga-Południe',
    'poland_warszawa_2020_rembertow.pb': 'Rembertów',
    'poland_warszawa_2020_srodmiescie.pb': 'Śródmieście',
    'poland_warszawa_2020_targowek.pb': 'Targówek',
    'poland_warszawa_2020_ursus.pb': 'Ursus',
    'poland_warszawa_2020_ursynow.pb': 'Ursynów',
    'poland_warszawa_2020_wawer.pb': 'Wawer',
    'poland_warszawa_2020_wesola.pb': 'Wesoła',
    'poland_warszawa_2020_wilanow.pb': 'Wilanów',
    'poland_warszawa_2020_wlochy.pb': 'Włochy',
    'poland_warszawa_2020_wola.pb': 'Wola',
    # 'poland_warszawa_2020_zoliborz.pb': 'Żoliborz'
}

REGION = {
    'warszawa_2023_geo': 'warszawa_2023',
    'warszawa_2022_geo': 'warszawa_2023',
    'warszawa_2021_geo': 'warszawa_2023',
    'warszawa_2020_geo': 'warszawa_2023',
    'warszawa_2023': 'warszawa_2023',
    'warszawa_2022': 'warszawa_2023',
    'warszawa_2021': 'warszawa_2023',
    'warszawa_2020': 'warszawa_2023',
}


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


def jaccard_distance(ac1, ac2):
    if len(ac1.union(ac2)) != 0:
        return 1 - len(ac1.intersection(ac2)) / len(ac1.union(ac2))
    return 0


def compute_distances(projects, acs):

    distances = {project_id: {} for project_id in projects}

    for project_id_1 in projects:
        ac1 = acs[str(project_id_1)]
        for project_id_2 in projects:
            if project_id_2 == project_id_1:
                continue
            ac2 = acs[str(project_id_2)]
            distances[str(project_id_1)][str(project_id_2)] = jaccard_distance(ac1, ac2)
            # distances[str(project_id_2)][str(project_id_1)] = distances[str(project_id_1)][str(project_id_2)]

    return distances


def convert_distances(distances):
    new_distances = np.zeros([len(distances), len(distances)])
    for p1, project_id_1 in enumerate(distances):
        for p2, project_id_2 in enumerate(distances[project_id_1]):
            new_distances[p1][p2] = distances[project_id_1][project_id_2]
            new_distances[p2][p1] = new_distances[p1][p2]

    return new_distances


def merge_images(list_of_names=None, size=250, show=False, ncol=1, nrow=1,
                 region=None):


    images = []
    for i, name in enumerate(list_of_names):
        images.append(Image.open(f'images/{region}/{name}.png'))
    image1_size = images[0].size

    new_image = Image.new('RGB', (ncol * image1_size[0], nrow * image1_size[1]),
                          (size, size, size))

    for i in range(ncol):
        for j in range(nrow):
            try:
                new_image.paste(images[i + j * ncol], (image1_size[0] * i, image1_size[1] * j))
            except:
                pass


    new_image.save(f'images/{region}.png', "PNG", quality=85)
    if show:
        new_image.show()

def import_original_winners(projects):
    winners = set()
    for project_id in projects:
        # print(projects[project_id])
        if projects[project_id]['selected'] == '1':
            winners.add(project_id)
    return winners


def prepare_region(region):

    geo = False
    if 'geo' in region:
        geo = True

    for name in NAMES[REGION[region]]:

        # print(name)
        path = f"data/{REGION[region]}/{name}"
        meta, projects, votes = import_data(path)

        acs = {project_id: set() for project_id in projects}

        for vote_id in votes:
            vote = ast.literal_eval(votes[vote_id]['vote'])
            if type(vote) == int:
                vote = [vote]
            for project_id in vote:
                acs[str(project_id)].add(str(vote_id))


        election = Election()
        election.read_from_files(path)

        winners_greedy = utilitarian_greedy(election)
        verify_cost(winners_greedy)
        winners_greedy = convert_winners(winners_greedy)

        election.binary_to_cost_utilities()
        winners_mes = equal_shares(election)
        verify_cost(winners_mes)
        winners_mes = convert_winners(winners_mes)

        # print(len(winners_mes), len(winners_greedy), len(winners_original))

        X = []
        Y = []
        S = []
        P = []
        #
        # for x, y in my_pos:
        #     X.append(x)
        #     Y.append(y)
        # for project_id in projects:
        #     cost = projects[project_id]['cost']
        #     cost = int(int(cost)/5000)+1
        #     S.append(cost*2)
        #     support = int((len(acs[project_id]))/10)+1
        #     P.append(support*2)

        voters_weight = {vote_id: 1 / len(votes[vote_id]) for vote_id in votes}

        S = []
        P = []

        if geo:

            X = []
            Y = []

            empty_list = []
            for project_id in projects:
                try:
                    lat = float(projects[project_id]['latitude'])
                    long = float(projects[project_id]['longitude'])
                    # print(lat, long)
                    # my_pos.append([lat, long])
                    X.append(long)
                    Y.append(lat)
                except:
                    empty_list.append(project_id)

        else:

            distances = compute_distances(projects, acs)
            distances = convert_distances(distances)

            size = len(distances[0])
            for i in range(size):
                for j in range(size):
                    distances[i][j] -= 0.5
                    if distances[i][j] < 0:
                        distances[i][j] = 0

            my_pos = MDS(n_components=2, dissimilarity='precomputed',
                         max_iter=100,
                         ).fit_transform(distances)
            for x, y in my_pos:
                X.append(x)
                Y.append(y)

        budget = int(meta['budget'])
        for project_id in projects:
            cost = int(projects[project_id]['cost'])
            # total_weight = sum(voters_weight[voter_id] for voter_id in acs[project_id])
            total_weight = len(acs[project_id])
            norm_support = budget / len(votes) * total_weight + 1
            print(project_id, norm_support)
            norm_cost = cost
            S.append(norm_cost / 700)
            P.append(norm_support / 700)

        plt.figure(figsize=(6.4, 6.4))
        empty_list = []

        for project_id,x,y,cost, support in zip(projects, X,Y,S,P):
            if project_id not in empty_list:
                # plt.scatter(x, y, s=cost, color='blue', alpha=0.6)
                # plt.scatter(x, y, s=support, color='purple', alpha=0.2)

                if project_id in winners_mes and project_id in winners_greedy:  # both
                    plt.scatter(x, y, s=cost, color='green', alpha=0.3, marker=MarkerStyle('o', fillstyle='left'))
                    plt.scatter(x, y, s=support, color='green', alpha=0.15, marker=MarkerStyle('o', fillstyle='right'))
                elif project_id in winners_mes and project_id not in winners_greedy:  # mes
                    plt.scatter(x, y, s=cost, color='blue', alpha=0.6, marker=MarkerStyle('o', fillstyle='left'))
                    plt.scatter(x, y, s=support, color='blue', alpha=0.4, marker=MarkerStyle('o', fillstyle='right'))
                elif project_id not in winners_mes and project_id in winners_greedy:  # greedy
                    plt.scatter(x, y, s=cost, color='red', alpha=0.6, marker=MarkerStyle('o', fillstyle='left'))
                    plt.scatter(x, y, s=support, color='red', alpha=0.4, marker=MarkerStyle('o', fillstyle='right'))
                else:  # none
                    plt.scatter(x, y, s=cost, color='grey', alpha=0.3, marker=MarkerStyle('o', fillstyle='left'))
                    plt.scatter(x, y, s=support, color='grey', alpha=0.1, marker=MarkerStyle('o', fillstyle='right'))


        plt.title(f'{NAMES[REGION[region]][name]}', size=30)
        plt.axis('off')

        plt.margins(0.1)
        plt.savefig(f'images/{region}/{name}.png',
                    # bbox_inches=Bbox([[-2, 0], [6.4+2, 6.4]]),
                    dpi=85*3)
        # plt.show()
        plt.clf()


# def prepare_region_geo(NAMES, region):
#
#     for name in NAMES[region]:
#         print(name)
#         path = f"data/{region}/{name}"
#         meta, projects, votes = import_data(path)
#
#         acs = {project_id: set() for project_id in projects}
#
#         for vote_id in votes:
#             vote = ast.literal_eval(votes[vote_id]['vote'])
#             if type(vote) == int:
#                 vote = [vote]
#             for project_id in vote:
#                 acs[str(project_id)].add(str(vote_id))
#
#         # distances = compute_distances(projects, acs)
#         # distances = convert_distances(distances)
#
#         # my_pos = []
#         election = Election()
#         election.read_from_files(path)
#
#         winners_greedy = utilitarian_greedy(election)
#         verify_cost(winners_greedy)
#         winners_greedy = convert_winners(winners_greedy)
#
#         election.binary_to_cost_utilities()
#         winners_mes = equal_shares(election)
#         verify_cost(winners_mes)
#         winners_mes = convert_winners(winners_mes)
#
#         winners_original = import_original_winners(projects)
#         if winners_greedy == winners_original:
#             print('same')
#         else:
#             print('diff')
#
#         print(len(winners_mes), len(winners_greedy), len(winners_original))
#         # print(len(winners_mes), len(winners_greedy))
#
#         # print(min(Y))
#         #   plt.scatter(lat, long)
#         # plt.show()

def compare_distances(NAMES, region):

    for name in NAMES[region]:
        # print(name)
        path = f"data/{region}/{name}"
        meta, projects, votes = import_data(path)

        acs = {project_id: set() for project_id in projects}

        for vote_id in votes:
            vote = ast.literal_eval(votes[vote_id]['vote'])
            if type(vote) == int:
                vote = [vote]
            for project_id in vote:
                acs[str(project_id)].add(str(vote_id))

        distances = compute_distances(projects, acs)
        # distances = convert_distances(distances)

        X = []
        Y = []

        # compute geo distances
        # geo_distances = {project_id: {} for project_id in projects}

        for project_id_1 in projects:
            for project_id_2 in projects:
                if project_id_2 == project_id_1:
                    continue
                try:
                    lat_1 = float(projects[project_id_1]['latitude'])
                    lat_2 = float(projects[project_id_2]['latitude'])
                    long_1 = float(projects[project_id_1]['longitude'])
                    long_2 = float(projects[project_id_2]['longitude'])
                    geo_distance = ((lat_1-lat_2)**2 + (long_1-long_2)**2)**0.5
                    jaccard_distance = distances[str(project_id_1)][str(project_id_2)]
                    # geo_distances[str(project_id_1)][str(project_id_2)] = geo_distance
                    # print(jaccard_distance)
                    # if jaccard_distance != 1:
                    X.append(geo_distance)
                    Y.append(jaccard_distance)

                except:
                    pass
                    # geo_distances[str(project_id_1)][str(project_id_2)] = None

        pcc = round(stats.pearsonr(X, Y)[0], 4)
        print(pcc, NAMES[region][name])
        plt.scatter(X, Y, alpha=0.1)
        plt.show()

        # return distances

def convert_winners(winners):
    new_winners = set()
    for w in winners:
        new_winners.add(w.idx)
    return new_winners


def verify_cost(winners):
    total = 0
    for w in winners:
        total += w.cost
    # print(total)


def analyze_region(region):

    for name in NAMES[REGION[region]]:

        # print(name)
        path = f"data/{REGION[region]}/{name}"
        meta, projects, votes = import_data(path)

        acs = {project_id: set() for project_id in projects}

        for vote_id in votes:
            vote = ast.literal_eval(votes[vote_id]['vote'])
            if type(vote) == int:
                vote = [vote]
            for project_id in vote:
                acs[str(project_id)].add(str(vote_id))

        election = Election()
        election.read_from_files(path)

        winners_greedy = utilitarian_greedy(election)
        verify_cost(winners_greedy)
        winners_greedy = convert_winners(winners_greedy)

        election.binary_to_cost_utilities()
        winners_mes = equal_shares(election)
        verify_cost(winners_mes)
        winners_mes = convert_winners(winners_mes)

        X = []
        Y = []
        S = []
        P = []


        distances = compute_distances(projects, acs)
        # print(distances)

        # mapping = {}
        # for i, project_id in enumerate(distances):
        #     mapping[str(project_id)] = i
        #

        empty_list = []

        group_A = []
        group_B = []
        group_C = []
        group_D = []

        for project_id in projects:
            if project_id in winners_mes and project_id in winners_greedy:  # both
                group_A.append(project_id)

            elif project_id in winners_mes and project_id not in winners_greedy:  # mes
                group_B.append(project_id)

            elif project_id not in winners_mes and project_id in winners_greedy:  # greedy
                group_C.append(project_id)

            else:  # none
                group_D.append(project_id)

        fig, ax = plt.subplots()
        matrix = np.zeros([5, 5])

        groups = {'Both': group_A,
                  'MES': group_B,
                  'Greedy': group_C,
                  'None': group_D,
                  'All': projects,}

        print(group_A, group_B)

        for i, group_id1 in enumerate(groups):
            g1 = groups[group_id1]
            for j, group_id2 in enumerate(groups):
                g2 = groups[group_id2]
                total = 0
                ctr = 0
                for project_id1 in g1:
                    for project_id2 in g2:
                        if project_id1 != project_id2:
                            dist = distances[str(project_id1)][str(project_id2)]
                            total += dist
                            ctr += 1
                print(group_id1, group_id2, total/ctr)
                c = round(total/ctr, 3)

                color = "black"
                # if c >= threshold:
                #     color = "white"
                c = str(c)
                if c[0] == '0':
                    c = c[1:]
                if c[-1] == '0' and c[-2] == '.':
                    c = c[:-1]
                ax.text(j, i, str(c), va='center', ha='center', color=color,
                        # size=ms
                        )
                matrix[i][j] = c

        ######

        # for i, family_id_1 in enumerate(selected_families):
        #     for j, family_id_2 in enumerate(selected_families):
        #         c = matrix[family_id_1][family_id_2]
        #         matrix_new[i][j] = c

        #
        # labels = []
        # for family_id in selected_families:
        #     if family_id in RULE_NAME_MATRIX:
        #         labels.append(RULE_NAME_MATRIX[experiment.families[family_id].label])
        #     elif family_id in SHORT_NICE_NAME:
        #         labels.append(SHORT_NICE_NAME[experiment.families[family_id].label])
        #     else:
        #         labels.append(experiment.families[family_id].label)

        ax.matshow(matrix, cmap=plt.cm.Blues,
                   # vmin=vmin, vmax=vmax
                   )

        #
        labels = ['Both', 'MES', 'Greedy', 'None', 'All']
        x_values = labels
        y_values = labels
        y_axis = np.arange(0, 5, 1)
        x_axis = np.arange(0, 5, 1)
        #
        # if yticks != 'none':
        #     ax.set_yticks(y_axis)
        #     if yticks == 'left':
        #         ax.set_yticklabels(y_values, rotation=25, size=ms + 2)
        #     if yticks == 'right':
        #         ax.set_yticklabels(y_values, rotation=-25, size=ms + 2)
        #         ax.yaxis.tick_right()
        # else:
        #     ax.set_yticks([])
        #
        ax.set_yticks(y_axis)
        ax.set_xticks(x_axis)
        ax.set_xticklabels(x_values, rotation=80, size=10 + 2)
        ax.set_yticklabels(y_values, size=10 + 2)
        #
        # if title:
        #     plt.title(title)
        #
        # if saveas and experiment.store:
        #     file_name = os.path.join(os.getcwd(), "images", str(saveas) + ".png")
        plt.savefig('similarity', bbox_inches='tight', dpi=200)
        #
        # if show:
        plt.show()



if __name__ == "__main__":
    regions = ['warszawa_2023', 'warszawa_2022', 'warszawa_2021', 'warszawa_2020',
               'warszawa_2023_geo', 'warszawa_2022_geo', 'warszawa_2021_geo', 'warszawa_2020_geo',
               ]
    regions = ['warszawa_2023']

    for region in regions:
        instance_type = 'approval'

        analyze_region(region)
