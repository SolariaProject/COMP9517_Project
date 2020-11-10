# convert annotation label

import cv2
import os
from matplotlib import pyplot as plt
import numpy as np


folder='./task3_dataset/annotation'
save_folder='./task3_dataset/annotation_labeled'
for i in os.listdir(folder):
    path=os.path.join(folder,i)
    img=cv2.imread(path)
    color=np.unique(img.reshape(-1, img.shape[2]), axis=0)
    for k in range(len(color)):
        img=np.where(img==color[k], [k,0,0], img).astype(np.uint8)
    cv2.imwrite(os.path.join(save_folder, i), img)