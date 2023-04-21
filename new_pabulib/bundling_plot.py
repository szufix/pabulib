import sys
from glossary import *
from _utils import *
import itertools
import copy
import os


if __name__ == "__main__":

    if len(sys.argv) < 2:
        regions = [
            'warszawa_2021',
        ]
    else:
        regions = [str(sys.argv[1])]

    for region in regions:

        print('Name;Win, Win;Win, Lose;Lose, Lose;0')
        for name in NAMES[region]:

            csv_name = name.replace('.pb', '.csv')
            path = os.path.join(os.getcwd(), "bundling", region, csv_name)
            with open(path, 'r', newline='') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')
                greedy, mes = reader

                col_1 = float(greedy['win, both win']) / \
                        (float(greedy['win, both win']) + float(greedy['lose, both win']))
                col_2 = float(greedy['win, single win']) / \
                        (float(greedy['win, single win']) + float(greedy['lose, single win']))
                col_3 = float(greedy['win, both lose']) / \
                        (float(greedy['win, both lose']) + float(greedy['lose, both lose']))

                print(f'{NAMES[region][name]} (Gr.);{col_1};{col_2};{col_3};0')

                col_1 = float(mes['win, both win']) / \
                        (float(mes['win, both win']) + float(mes['lose, both win']))
                col_2 = float(mes['win, single win']) / \
                        (float(mes['win, single win']) + float(mes['lose, single win']))
                col_3 = float(mes['win, both lose']) / \
                        (float(mes['win, both lose']) + float(mes['lose, both lose']))

                print(f'{NAMES[region][name]} (MES);{col_1};{col_2};{col_3};1')

