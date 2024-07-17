
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt

from scipy.stats import spearmanr, pearsonr

from glossary import NAMES


if __name__ == "__main__":




    # for name in NAMES[f'warszawa_2019t']:
    # for name in NAMES[f'warszawa_2024d']:
    # for name in NAMES[f'mt_knapsack']:
    for name in NAMES[f'mt_k']:

        try:

            data = []

            print(name)
            path = f'pabulib_877/{name}'
            instance, profile = parse_pabulib(path)

            for v in profile:
                data.append(len(v))

            COSTS = []
            SUPPORT = []

            for p in instance.project_meta:
                support = float(instance.project_meta[p]['votes'])
                SUPPORT.append(support)
                cost = float(instance.project_meta[p]['cost'])
                COSTS.append(cost)

            keynote_blue = '#007AFF'
            keynote_red = '#FF2D55'

            plt.rcParams['font.family'] = 'Helvetica Neue'
            plt.rcParams['font.size'] = 12

            plt.scatter(COSTS, SUPPORT, color=keynote_blue)




            # add linear regression line
            from numpy import polyfit
            from numpy import poly1d
            p = polyfit(COSTS, SUPPORT, 1)
            f = poly1d(p)
            # set marker color to keynote_blue
            plt.plot(COSTS, f(COSTS), 'r')

            plt.ylim([-3,53])

            pearson_corr, pearson_p_value = pearsonr(COSTS, SUPPORT)
            print(f"Pearson Correlation: {pearson_corr:.2f}, P-value: {pearson_p_value:.4f}")

            # plt.savefig(f'pcc/pcc_{name.replace(".","_")}.png', bbox_inches='tight', dpi=200)
            # plt.show()
        except:
            print(f'Failed for {name}')

