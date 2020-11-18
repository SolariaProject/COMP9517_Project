#!/bin/bash
ARA2012_PATH="./datasets/Plant/Ara2012/"
ARA2013_PATH="./datasets/Plant/Ara2013-Canon/"
TOBACCO_PATH="./datasets/Plant/Tobacco/"

IMG_SUFFIX="*_rgb.png"
LABEL_SUFFIX="*_label.png"

TASK3_PATH="task3_dataset"

if [ -d $TASK3_PATH ]
then
    echo "folder exists"
else
    mkdir $TASK3_PATH
    mkdir $TASK3_PATH/images
    cp $ARA2012_PATH$IMG_SUFFIX $TASK3_PATH/images/
    cp $ARA2013_PATH$IMG_SUFFIX $TASK3_PATH/images/
    cp $TOBACCO_PATH$IMG_SUFFIX $TASK3_PATH/images/
    for f in $TASK3_PATH/images/*; do
        newname=`echo "$f" | sed 's/_rgb//g'`
        mv "$f" "$newname"
    done

    mkdir $TASK3_PATH/annotation
    cp $ARA2012_PATH$LABEL_SUFFIX $TASK3_PATH/annotation/
    cp $ARA2013_PATH$LABEL_SUFFIX $TASK3_PATH/annotation/
    cp $TOBACCO_PATH$LABEL_SUFFIX $TASK3_PATH/annotation/
    for f in $TASK3_PATH/annotation/*; do
        newname=`echo "$f" | sed 's/_label//g'`
        mv "$f" "$newname"
    done
fi