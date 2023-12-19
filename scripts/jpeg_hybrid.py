#!/usr/bin/env python3
"""Creates JPEG grid on processed images for the hybrid dataset"""
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
        if (folder / 'hybrid_select_0.png').exists() and (
                folder / 'hybrid_select_1.png').exists():
            continue
        tbar.write(folder.name)
        with open(folder / 'gt_hybrid_select.txt', 'r') as f:
            f.readline()
            jpeg_line = f.readline().split()
        # Get the qualities and offsets from the ground truth
        if jpeg_line[1] == "None":  # No JPEG compression to perform
            for i in (0, 1):
                im = imageio.imread(folder / f'hybrid_select_p_{i}.png')
                imageio.imsave(folder / f'hybrid_select_{i}.png', im)
            continue
        elif jpeg_line[0] == "JPEGGrid":
            quality0, δy, δx = map(int, jpeg_line[1:])
            quality1 = quality0
        elif jpeg_line[0] == "JPEGQual":
            quality0, quality1, δy, δx = map(int, jpeg_line[1:])
        else:
            raise ValueError(jpeg_line)
        # first image
        Im = Image.open(folder / 'hybrid_select_p_0.png')
        im = np.array(Im)
        buffer = io.BytesIO()
        Im.save(buffer, "JPEG", quality=quality0)
        img_0 = np.array(Image.open(buffer))
        imageio.imwrite(folder / 'hybrid_select_0.png', img_0)

        # second image
        Im = Image.open(folder / 'hybrid_select_p_1.png')
        im = np.array(Im)
        extended_image = np.pad(im, ((8, 0), (8, 0), (0, 0)), 'symmetric')
        im1 = Image.fromarray(extended_image[δy:, δx:])
        buffer = io.BytesIO()
        im1.save(buffer, "JPEG", quality=quality1)
        im1_compressed = np.array(Image.open(buffer))
        img_1 = im1_compressed[8 - δy:, 8 - δx:]
        imageio.imwrite(folder / 'hybrid_select_1.png', img_1)


if __name__ == "__main__":
    main()
