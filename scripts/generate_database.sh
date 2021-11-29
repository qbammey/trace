#!/usr/bin/env bash

python make_gt_global
python make_gt_noise.py
python make_gt_cfa
python make_gt_jpeg.py
python make_gt_hybrid.py
python process_nef.py
python segment.py
python create_forgery_masks.py
python merge_images.py

