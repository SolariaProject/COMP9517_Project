import numpy as np
import cv2
import os

path_base = './task3_dataset/annotation/'
filenames = [path_base + f for f in os.listdir(path_base)]
images = [cv2.imread(f, cv2.IMREAD_GRAYSCALE) for f in filenames]
borders = []

for i in images:
    colors = np.unique(i)[1:]
    contours=[cv2.findContours(np.where(i == c, 255, 0).astype(np.uint8), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)[0] for c in colors]
    
    for cnts in range(len(contours)):
        print('color: '+ str(cnts))
        for k in contours[cnts]:
            k=k.reshape(-1,2)
            poly = [(x + 0.5, y + 0.5) for x, y in zip(k[:,0], k[:,1])]
            print(len(poly))


# check the borders
# try:
#     os.mkdir('borders')
# except Exception:
#     pass
# for img_idx, b in enumerate(borders):
#     for obj_idx, o in enumerate(b):
#         cv2.imwrite('borders\{}_{}.png'.format(img_idx, obj_idx), o)
