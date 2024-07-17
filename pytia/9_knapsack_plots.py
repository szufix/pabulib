
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt

from glossary import NAMES


if __name__ == "__main__":


    # for name in NAMES[f'warszawa_2019t']:
    # for name in NAMES[f'amsterdam_252']:
    # for name in NAMES[f'wroclaw_2020c']:
    # for name in NAMES[f'warszawa_2024c']:
    # for name in NAMES[f'wieliczka_2023c']:
    for name in NAMES[f'krakow_2023c']:

        try:
            data = []
            print(name)
            path = f'pabulib_877/{name}'
            instance, profile = parse_pabulib(path)

            for v in profile:
                data.append(len(v))

            X = []
            # for each voter compute the sum of the costs of supported projects
            for v in profile:
                cost = 0
                for p in v:
                    cost += float(instance.project_meta[p]['cost'])
                X.append(cost)


            print(len(X))

            # print the histogram of X

            keynote_blue = '#007AFF'

            plt.rcParams['font.family'] = 'Helvetica Neue'
            plt.rcParams['font.size'] = 14

            # create a histogram with 20 bins, and return the number of elements in each bin


            n, bins, patches = plt.hist(X, bins=20, color=keynote_blue, edgecolor='black')

            print(n[-1]/len(X))

            # plt.savefig(f'sscw/knapsack_warszawa_2019t', bbox_inches='tight', dpi=200)
            # plt.savefig(f'sscw/knapsack_amsterdam_252', bbox_inches='tight', dpi=200)
            # plt.savefig(f'sscw/wroclaw_2020c_bundle', bbox_inches='tight', dpi=200)
            # plt.savefig(f'sscw/warszawa_2024c_bundle', bbox_inches='tight', dpi=200)
            # plt.savefig(f'sscw/wieliczka_2023c_bundle', bbox_inches='tight', dpi=200)
            plt.savefig(f'sscw/krakow_2023c_bundle', bbox_inches='tight', dpi=200)
            plt.show()



        except:
            print(f'Failed for {name}')

