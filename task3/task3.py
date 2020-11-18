from detectron2.utils.visualizer import ColorMode
import detectron2

# import some common libraries
import numpy as np
import os
import json
import cv2
import random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

from detectron2.structures import BoxMode

from detectron2.utils.visualizer import ColorMode


def get_leaf_dicts(img_dir):
    img_dir = os.path.join("task3",img_dir) # for running in project root
    json_file = os.path.join(img_dir, "via.json")
    with open(json_file) as f:
        imgs_anns = json.load(f)

    dataset_dicts = []
    for idx, v in enumerate(imgs_anns.values()):
        record = {}

        filename = os.path.join(img_dir, "images", v["filename"])
        height, width = cv2.imread(filename).shape[:2]

        record["file_name"] = filename
        record["image_id"] = idx
        record["height"] = height
        record["width"] = width

        annos = v["regions"]
        objs = []
        for _, anno in annos.items():
            assert not anno["region_attributes"]
            anno = anno["shape_attributes"]
            px = anno["all_points_x"]
            py = anno["all_points_y"]
            poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
            poly = [p for x in poly for p in x]
            obj = {
                "bbox": [np.min(px), np.min(py), np.max(px), np.max(py)],
                "bbox_mode": BoxMode.XYXY_ABS,
                "segmentation": [poly],
                "category_id": 0,
            }
            objs.append(obj)
        record["annotations"] = objs
        dataset_dicts.append(record)
    return dataset_dicts


for d in ["train", "val"]:
    DatasetCatalog.register(
        "leaf_" + d, lambda d=d: get_leaf_dicts("leaf/" + d + "/"))
    MetadataCatalog.get("leaf_" + d).set(thing_classes=["leaf"])
leaf_metadata = MetadataCatalog.get("leaf_train")


cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TRAIN = ("leaf_train",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.DEVICE='cpu'

cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Let training initialize from model zoo
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
cfg.SOLVER.MAX_ITER = 2000
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 512
# only has one class. (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1

# path to the model we just trained
cfg.MODEL.WEIGHTS = os.path.join("./task3/output", "model_final.pth") # running in project root
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
predictor = DefaultPredictor(cfg)


dataset_dicts = get_leaf_dicts("leaf/val")

os.mkdir('task3_out') 

for d in filter(lambda val: "plant007" in (val['file_name']), dataset_dicts):
    # for d in dataset_dicts:
    im = cv2.imread(d["file_name"])
    # format is documented at https://detectron2.readthedocs.io/tutorials/models.html#model-output-format
    outputs = predictor(im)
    v = Visualizer(im[:, :, ::-1],
                   metadata=leaf_metadata,
                   scale=1,
                   # remove the colors of unsegmented pixels. This option is only available for segmentation models
                   instance_mode=ColorMode.IMAGE_BW
                   )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    bitmask = outputs['instances'].pred_masks
    n, x, y = bitmask.shape
    mask = np.zeros((x, y, 3), dtype=np.uint8)
    for i in range(n):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        img = np.where(bitmask[i].to("cpu") == True, 255, 0)
        mask[img == 255] = [b, g, r]

    # cv2_imshow(mask)
    fname = os.path.basename(d['file_name'])
    cv2.imwrite('task3_out/rgb_mask_'+fname, mask)
    cv2.imwrite('task3_out/'+fname, out.get_image()[:, :, ::-1])
    # cv2_imshow(out.get_image()[:, :, ::-1])
