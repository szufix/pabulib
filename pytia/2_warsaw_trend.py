
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt


def print_warsaw_trend():

    outcome = []

    for year in [2020, 2021, 2022, 2023, 2024, 2025]:
        print(year)
        data = []
        path = f'pabulib/poland_warszawa_{year}_.pb'
        instance, profile = parse_pabulib(path)

        for v in profile:
            data.append(len(v))

        # count how many votes have length 10
        bars = [0 for _ in range(0, 11)]
        for d in data:
            bars[d] += 1
        max_vote = bars[10]/sum(bars)
        outcome.append(max_vote)
        
        print(outcome)

    plt.plot(outcome)
    plt.show()

    # X_names = [
    #     '1', '2', '3', '4', '5'
    # ]
    # #
    #
    # keynote_blue = '#007AFF'
    # plt.rcParams['font.family'] = 'Helvetica Neue'
    # plt.rcParams['font.size'] = 18
    #
    # plt.hist(data, bins=5, range=(1, 6), color=keynote_blue, edgecolor='black')
    #
    # ticks = [i + 0.5 for i in range(1, 6)]
    # plt.xticks(ticks, X_names, fontsize=24)
    #
    # # plt.title("Histogram of lengths of votes")
    # plt.savefig(f'stanford_img/{stanford_name}', bbox_inches='tight', dpi=200)
    # plt.show()


if __name__ == "__main__":

    print_warsaw_trend()
