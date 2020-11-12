import numpy as np
import cv2
import os
import json

path_origin_base = './task3_dataset/annotation/'


def gen_via_json(path_base: str):
    """ 
    Generate JSON file for training, 
    this function will tries to find the contours of each leaf in every images
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
        contours = [
            cv2.findContours(
                image=np.where(i == c, c, 0).astype('uint8'),
                mode=cv2.RETR_EXTERNAL,
                method=cv2.CHAIN_APPROX_SIMPLE
            )[0][0].reshape(-1, 2) for c in colors # for opencv4.0 there are only 2 return value.
        ]

        # at least three points
        contours = [c for c in contours if len(c) >= 3]

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
            x = c[:, 0].tolist()
            y = c[:, 1].tolist()
            this_region["all_points_x"], this_region["all_points_y"] = x, y

    with open('via.json', 'w') as outfile:
        outfile.write(json.dumps(roots))


gen_via_json(path_origin_base)
