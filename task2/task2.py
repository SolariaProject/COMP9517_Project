from sklearn.model_selection import train_test_split
import os
import numpy as np
import cv2
from scipy.cluster.vq import *
from sklearn.svm import LinearSVC
from sklearn import metrics
from collections import defaultdict



if __name__=='__main__':
    path1='./Plant_Phenotyping_Datasets/Tray/Ara2012'
    path2='./Plant_Phenotyping_Datasets/Tray/Ara2013-Canon'
    file2012='/ara2012_tray02_rgb.png'
    target2012='/ara2012_tray02_fg.png'
    file2013='/ara2013_tray03_rgb.png'
    target2013='/ara2013_tray03_fg.png'
    sample_img=cv2.imread(path2+file2013)
    sample_target=cv2.imread(path2+target2013,0)

    #cv2.imshow('1',imgs_1[1])
    #cv2.imshow('2', targets_1[1])
    #cv2.waitKey(0)

    lower_green = np.array([36, 43, 106])
    upper_green = np.array([77, 255, 255])
    hsv = cv2.cvtColor(sample_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lowerb=lower_green,upperb=upper_green)
    #des=cv2.fastNlMeansDenoising(mask,None,10,10,7,21)
    cv2.imwrite('mask.png', mask)
    median = cv2.medianBlur(mask, 5)
    cv2.imwrite('median.png',median)


    q = defaultdict(int)
    for x in range(sample_target.shape[0]):
        for y in range(sample_target.shape[1]):
            if sample_target[x][y] == 0 and median[x][y] == 0:
                q['tn'] += 1
            if sample_target[x][y] == 255 and median[x][y] == 0:
                q['fn'] += 1
            if sample_target[x][y] == 0 and median[x][y] == 255:
                q['fp'] += 1
            if sample_target[x][y] == 255 and median[x][y] == 255:
                q['tp'] += 1

    dice = (2 * q['tp']) / (q['fn'] + q['fp'] + 2 * q['tp'])
    iou = q['tp'] / ( q['fp'] + q['tp'] + q['fn'])
    print('dice:',dice)
    print('IOU:',iou)



