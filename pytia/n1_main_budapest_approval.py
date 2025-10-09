from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt

from glossary import NAMES


def print_budapest_citywide(year, cutoff=10):

    data = []

    path = f'budapest/budapest_2025_pre-voting_v1.2.pb'
    instance, profile = parse_pabulib(path)

    for v in profile:
        data.append(len(v))

    num_votes = len(data)
    num_projects = len(instance)
    # Calculate and print average vote length
    print(num_votes, num_projects)
    if data:
        avg_length = sum(data) / num_votes
        print(f"Average vote length: {avg_length:.2f}")
        saturation = sum(data) / num_votes /  num_projects
        print(f"Saturation: {saturation:.2f}")
    else:
        print("No votes found.")


    bars = [0 for _ in range(0, cutoff+1)]
    for i, d in enumerate(data):
        if d>cutoff:
            d=cutoff
            data[i] = cutoff
        bars[d] += 1
    # for i in range(1, cutoff+1):
    #     print(f'{i}, ', end='')
    # print('')
    # print(bars[1:cutoff+1])
    # print(bars[1]/sum(bars))


    keynote_blue = '#007AFF'
    plt.rcParams['font.family'] = 'Helvetica Neue'
    plt.rcParams['font.size'] = 14

    plt.hist(data, bins=cutoff, range=(1, cutoff+1), color=keynote_blue, edgecolor='black')

    ticks = [i + 0.5 for i in range(1, cutoff+1)]
    # plt.xticks(ticks, X_names)
    plt.ylim([0, 3500])

    # plt.title("Histogram of lengths of votes")
    plt.savefig(f'dagstuhl/budapest_{year}c', bbox_inches='tight', dpi=200)
    plt.show()



if __name__ == "__main__":

    print_budapest_citywide(2025, cutoff=100)
