import cv2

img_array = []

step = 10

PATH = '/Users/szufa/PycharmProjects/pabulib/pb_cost/images/games/warszawa_2023/'
# num_rounds = 1000
# base = 'poland_warszawa_2023_rembertow_greedy_cost_sat_'
# num_rounds = 1000
# base = 'poland_warszawa_2023_wesola_greedy_cardinality_sat_'
# num_rounds = 1000
# base = 'poland_warszawa_2023_wesola_phragmen_'
num_rounds = 1000
base = 'poland_warszawa_2023_wesola_mes_phragmen_'

for r in range(num_rounds):
    if r % 10 == 0:
        filename = PATH + base + str(r) + '.png'
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

out = cv2.VideoWriter(f'movies/{base}.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 40, size)


for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
