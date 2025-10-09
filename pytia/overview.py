
import os
import csv

import matplotlib.pyplot as plt



if __name__ == "__main__":

    # import data from pabulib_params.csv
    # and plot the first two columns as scatter plot
    with open('pabulib_params.csv', 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = next(reader)
        x = []
        y = []
        for row in reader:
           x.append(int(row[0]))
           y.append(int(row[1]))


    plt.scatter(x, y, alpha=0.33)
    plt.xlabel('num_candidates')
    plt.ylabel('num_voters')
    plt.savefig("pabulib_params", dpi=200, bbox_inches='tight')