#!/usr/bin/env python3
"""Create the ground truth for the JPEG grid and JPEG Quality datasets."""

import random
from pathlib import Path

MIN_QUALITY = 75
MAX_QUALITY = 100

if __name__ == "__main__":
    random.seed(0)
    folders = sorted(Path('../images/').glob('*'))
    for folder in folders:
        quality = random.randint(MIN_QUALITY, MAX_QUALITY)
        δ_flat = random.randint(1, 63)
        δy = δ_flat // 8
        δx = δ_flat % 8
        open(folder / 'gt_jpeg_grid.txt', 'w').write(f'{quality}\n{δy} {δx}')
        quality_0 = random.randint(MIN_QUALITY, MAX_QUALITY)
        quality_1 = quality_0
        while quality_1 == quality_0:
            quality_1 = random.randint(MIN_QUALITY, MAX_QUALITY)
        δy, δx = random.randint(0, 7), random.randint(0, 7)
        open(folder / 'gt_jpeg_quality.txt',
             'w').write(f'{quality_0}\n{quality_1} {δy} {δx}')
