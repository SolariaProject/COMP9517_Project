import numpy as np
import cv2
import os
import json
from pprint import pprint

<<<<<<< HEAD
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
=======
path_origin_base = './task3_dataset/annotation/'


def gen_coco_json(path_base: str):
    """ 
    Generate JSON file for training, 
    this function will tries to find the contour of each leaf in every images
    and record them into JSON file in required format
    """
    # read images from given directory
    file_paths = [path_base + f for f in os.listdir(path_base)]
    images = [cv2.imread(f, cv2.IMREAD_GRAYSCALE) for f in file_paths]

    # construct dictionary
    roots = {}
    for p in os.listdir(path_base):
        key_of_root = p + str(os.path.getsize(path_base + p))
        roots[key_of_root] = {
            "fileref": "",
            "size": os.path.getsize(path_base + p),
            "filename": p,
            "base64_img_data": "",
            "file_attributes": {}
        }

    # find contour and put them into dictionary
    for i, k in zip(images, roots):
        # find countours of different leaves
        colors = np.unique(i)[1:]
        contours = [cv2.Canny(np.where(i == c, c, 0).astype(
            'uint8'), 0, 255) for c in colors]

        # put them into dictionary
        this = roots[k]
        this["regions"] = {str(i): {
            "shape_attributes": {
                "name": "polygon"
            },
            "region_attributes": {}
        } for i in range(0, len(contours))}

        for idx, c in enumerate(contours):
            this_region = this["regions"][str(idx)]["shape_attributes"]
            y, x = np.where(c == 255)
            y, x = y.tolist(), x.tolist()
            this_region["all_points_x"], this_region["all_points_y"] = x, y

    with open('coco.json', 'w') as outfile:
        outfile.write(json.dumps(roots))


gen_coco_json(path_origin_base)
>>>>>>> c6f0bc9d0e3979eece0eb3174b24e4d7ac9ef367
