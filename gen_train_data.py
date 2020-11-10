import numpy as np
import cv2
import os

path_base = './task3_dataset/annotation/'
filenames = [path_base + f for f in os.listdir(path_base)]
images = [cv2.imread(f, cv2.IMREAD_GRAYSCALE) for f in filenames]
borders = []

for i in images:
    colors = np.unique(i)[1:]
    borders.append([cv2.Canny(np.where(i == c, c, 0).astype('uint8'), 0, 255) for c in colors])

# check the borders
# try:
#     os.mkdir('borders')
# except Exception:
#     pass
# for img_idx, b in enumerate(borders):
#     for obj_idx, o in enumerate(b):
#         cv2.imwrite('borders\{}_{}.png'.format(img_idx, obj_idx), o)
