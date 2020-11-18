# COMP9517_Project
## Task 3

**requirements**: 

```bash
pip install split-folders 
pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.7/index.html (depends on pytorch version)
```

**structure**:

task3_data.sh: copy to new folder and construct new structure for Detectron2

gen_train_data.py: convert RGB mask to VIA json format

task3.py: predict from command

preprocessed dataset: [Google Drive](https://drive.google.com/file/d/1CaWySqbCG6Qceq-lOnlImHaAIf4x7qfr/view?usp=sharing)

training code: [segnet-keras](https://github.com/divamgupta/image-segmentation-keras)

leaf/: folder for preprocessed training and testing datasets

output/: folder for output files from Detectron2 (including trained model and metrics)

val_pred/: folder for predictions including bbox AR images and RGB mask images
