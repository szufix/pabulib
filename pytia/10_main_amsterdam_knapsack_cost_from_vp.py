
from pabutools.election import parse_pabulib

import matplotlib.pyplot as plt

from glossary import NAMES


if __name__ == "__main__":


    for name in NAMES[f'warszawa_2019t']:
    # for name in NAMES[f'warszawa_2020d']:

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

            # create a list of 10% of the cheapest projects
            COSTS.sort()
            ten_percent = int(len(COSTS) * 0.1)
            cheapest = COSTS[:ten_percent]
            # create a list of 10% of the most expensive projects
            COSTS.sort(reverse=True)
            most_expensive = COSTS[:ten_percent]

            # count the ration of voters that supported at least of the cheapest projects
            count_cheapest_supporters = 0
            for v in profile:
                for p in v:
                    if float(instance.project_meta[p]['cost']) in cheapest:
                        count_cheapest_supporters += 1
                        break

            # count the ration of voters that supported at least of the expesive projects
            count_expensive_supporters = 0
            for v in profile:
                for p in v:
                    if float(instance.project_meta[p]['cost']) in most_expensive:
                        count_expensive_supporters += 1
                        break

            print(f'Cheapest: {count_cheapest_supporters / len(profile)}')
            # print(f'Most expensive: {count_expensive_supporters / len(profile)}')


        except:
            print(f'Failed for {name}')

