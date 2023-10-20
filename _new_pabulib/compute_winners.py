import csv
import matplotlib.pyplot as plt
import ast
from scipy.stats import stats
import math
from pabutools.rules import equal_shares, utilitarian_greedy
from pabutools.model import Election


def convert_winners(winners):
    new_winners = set()
    for w in winners:
        new_winners.add(w.idx)
    return new_winners


if __name__ == "__main__":

    election = Election().read_from_files('data/warszawa_2020/poland_warszawa_2020_bemowo.pb')

    winners_mes = equal_shares(election)
    winners_mes = convert_winners(winners_mes)

    winners_greedy = utilitarian_greedy(election)
    winners_greedy = convert_winners(winners_greedy)

    print(winners_mes, winners_greedy)





