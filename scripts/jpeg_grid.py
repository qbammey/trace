#!/usr/bin/env python3
"""Creates JPEG grid on processed images for the jpeg_grid dataset."""

from pathlib import Path
import glob
import io
from tqdm import tqdm
import imageio
import numpy as np
from PIL import Image


def main():
    folders = sorted(map(Path, glob.glob('../images/*')))
    tbar = tqdm(folders, leave=True, position=0, dynamic_ncols=True)

    for folder in tbar:
        if (folder / 'jpeg_grid_0.png').exists() and (
                folder / 'jpeg_grid_1.png').exists():
            continue
        tbar.write(folder.name)
        Im = Image.open(folder / 'cfa_0.png')
        im = np.array(Im)

        # create extended image with 8 additionnal columns and rows
        extended_image = np.pad(im, ((8, 0), (8, 0), (0, 0)), 'symmetric')

        # Read the ground truth
        with open(folder / 'gt_jpeg_grid.txt', 'r') as f:
            quality, = map(int, f.readline().split())
            δy, δx = map(int, f.readline().split())

        # create img_0
        buffer = io.BytesIO()
        Im.save(buffer, "JPEG", quality=quality)
        img_0 = np.array(Image.open(buffer))
        imageio.imwrite(folder / 'jpeg_grid_0.png', img_0)

        # create img_1
        im1 = Image.fromarray(extended_image[δy:, δx:])
        buffer = io.BytesIO()
        im1.save(buffer, "JPEG", quality=quality)
        im1_compressed = np.array(Image.open(buffer))
        img_1 = im1_compressed[8 - δy:, 8 - δx:]
        imageio.imwrite(folder / 'jpeg_grid_1.png', img_1)


if __name__ == "__main__":
    main()
