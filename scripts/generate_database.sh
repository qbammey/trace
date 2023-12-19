#!/usr/bin/env bash

python make_gt_global.py
python make_gt_noise.py
python make_gt_cfa.py
python make_gt_jpeg.py
python make_gt_hybrid.py
python process_nef.py
python jpeg_grid.py
python jpeg_quality.py
python jpeg_hybrid.py
python segment.py
python create_forgery_masks.py
python merge_images.py

