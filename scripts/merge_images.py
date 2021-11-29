#!/usr/bin/env python3
"""Merge the two images into one using the forgery mask."""
import glob
from multiprocessing import Pool
from pathlib import Path

import imageio
import numpy as np
from tqdm import tqdm

folders = sorted(list(map(Path, glob.glob('../images/*'))))


def merge(folder, mask, img0, img1, dest):
    img0 = imageio.imread(folder / img0)
    img1 = imageio.imread(folder / img1)
    img = np.zeros_like(img0)
    img[mask == 0] = img0[mask == 0]
    img[mask > 0] = img1[mask > 0]
    imageio.imsave(folder / dest, img)


if __name__ == "__main__":
    tbar = tqdm(folders, leave=True, dynamic_ncols=True)
    pool = Pool(9)
    for suffix in ['_endo', '_exo']:
        for folder in tbar:
            tbar.write(folder.name)
            mask = imageio.imread(folder / f'mask{suffix}.png')
            if not (folder / f'cfa_grid{suffix}.png').exists():
                pool.apply_async(merge, [
                    folder, mask, 'cfa_0.png', 'cfa_grid_1.png',
                    f'cfa_grid{suffix}.png'
                ])
            if not (folder / f'cfa_alg{suffix}.png').exists():
                pool.apply_async(merge, [
                    folder, mask, 'cfa_0.png', 'cfa_alg_1.png',
                    f'cfa_alg{suffix}.png'
                ])
            if not (folder / f'jpeg_grid{suffix}.png').exists():
                pool.apply_async(merge, [
                    folder, mask, 'jpeg_grid_0.png', 'jpeg_grid_1.png',
                    f'jpeg_grid{suffix}.png'
                ])
            if not (folder / f'jpeg_quality{suffix}.png').exists():
                pool.apply_async(merge, [
                    folder, mask, 'jpeg_quality_0.png', 'jpeg_quality_1.png',
                    f'jpeg_quality{suffix}.png'
                ])
            if not (folder / f'noise{suffix}.png').exists():
                pool.apply_async(merge, [
                    folder, mask, 'noise_0.png', 'noise_1.png',
                    f'noise{suffix}.png'
                ])
            if not (folder / f'hybrid_select{suffix}.png').exists():
                pool.apply_async(merge, [
                    folder, mask, 'hybrid_select_0.png', 'hybrid_select_1.png',
                    f'hybrid_select{suffix}.png'
                ])

    pool.close()
    pool.join()
