#!/usr/bin/env python3
"""Process the RAW images for the different datasets."""

from pathlib import Path

import imageio
import numpy as np
import rawpy
from rawpy import DemosaicAlgorithm as da
from scipy.ndimage import gaussian_filter1d
from tqdm import tqdm

σ = .3
padding = 32

offsets = {
    'RGGB': (0, 0),
    'GRBG': (0, 1),
    'GBRG': (1, 0),
    'BGGR': (1, 1),
}

demosaicing_algorithms = {
    'LINEAR': da.LINEAR,
    'VNG': da.VNG,
    'PPG': da.PPG,
    'AHD': da.AHD,
    'DCB': da.DCB,
    'MODIFIED_AHD': da.MODIFIED_AHD,
    'AFD': da.AFD,
    'VCD': da.VCD,
    'VCD_MODIFIED_AHD': da.VCD_MODIFIED_AHD,
    'LMMSE': da.LMMSE,
    'AMAZE': da.AMAZE,
    'DHT': da.DHT,
    'AAHD': da.AAHD
}


def process_one(folder, grid, algorithm, γ, noise_A=None, noise_B=None):
    filename = (folder / 'original.NEF').resolve().as_posix()
    raw = rawpy.imread(filename)
    data = raw.raw_image_visible.astype(np.float64)
    Y, X = data.shape
    Y -= Y % 2
    X -= X % 2
    data = data[:Y, :X]
    δy, δx = np.argwhere(raw.raw_colors == 0)[0]  # offset on the raw
    r = data[δy::2, δx::2]
    b = data[1 - δy::2, 1 - δx::2]
    g = .5 * (data[δy::2, 1 - δx::2] + data[1 - δy::2, δx::2])
    small_img = np.array([r, g, b]).transpose(1, 2, 0)
    small_img = gaussian_filter1d(gaussian_filter1d(small_img, σ, axis=0),
                                  σ,
                                  axis=1)
    tδy, tδx = offsets[grid]  # target offsets
    fδy, fδx = np.abs(tδy - δy), np.abs(
        tδx - δx)  # first pixel corresponding to real image
    small_img = np.pad(
        small_img, [(fδy, padding), (fδx, padding), (0, 0)], mode='reflect'
    )  # small image is padded so that raw image offset and target offset are the same
    if noise_A is not None and noise_B is not None:
        std = np.sqrt(noise_A + noise_B * small_img)
        z = np.random.normal(0, std).astype(small_img.dtype)
        z = np.maximum(
            z, -small_img)  # do not remove more than the number of photons
        small_img += z
        small_img[small_img > np.iinfo(np.uint16).max] = np.iinfo(
            np.uint16).max
    small_img = small_img.astype(np.uint16)
    Y, X, _ = small_img.shape
    data = raw.raw_image_visible[:Y, :X]
    data[δy::2, δx::2] = small_img[δy::2, δx::2, 0]  # red
    data[δy::2, 1 - δx::2] = small_img[δy::2, 1 - δx::2, 1]  # first green
    data[1 - δy::2, δx::2] = small_img[1 - δy::2, δx::2, 1]  # second green
    data[1 - δy::2, 1 - δx::2] = small_img[1 - δy::2, 1 - δx::2, 2]  # blue
    post = raw.postprocess(
        demosaic_algorithm=demosaicing_algorithms[algorithm],
        gamma=(γ, 4.5),
        user_flip=0,
        use_camera_wb=True)
    cut = post[fδy:Y - padding, fδx:X - padding]
    return cut


if __name__ == "__main__":
    folders = sorted(Path('../images/').glob('*'))
    tbar = tqdm(folders, leave=True, position=0, dynamic_ncols=True)
    for folder in tbar:
        tbar.write(folder.name)
        global_grid, algorithm, γ = open(folder / 'gt_global.txt',
                                         'r').readline().split()
        γ = float(γ)
        cfa_grid_grid = open(folder / 'gt_cfa_grid.txt',
                             'r').readline().split()[0]
        with open(folder / 'gt_noise.txt', 'r') as f:
            a0, b0 = map(float, f.readline().split())
            a1, b1 = map(float, f.readline().split())
        cfa_alg_grid, cfa_alg_alg = open(folder / 'gt_cfa_algorithm.txt',
                                         'r').readline().split()
        cfa_grid_1 = process_one(folder, cfa_grid_grid, algorithm,
                                 γ)  # cfa_1.png
        with open(folder / 'gt_hybrid_select.txt', 'r') as f:
            noise_line = f.readline().split()
            if noise_line[1] == "None":
                hybrid_select_noise_0_A, hybrid_select_noise_0_B = None, None
                hybrid_select_noise_1_A, hybrid_select_noise_1_B = None, None
            else:
                hybrid_select_noise_0_A, hybrid_select_noise_0_B, hybrid_select_noise_1_A, hybrid_select_noise_1_B = map(
                    float, noise_line[1:])
            jpeg_line = f.readline().split()
            cfa_line = f.readline().split()
            if cfa_line[1] == "None":
                hybrid_select_grid = global_grid
                hybrid_select_algorithm = algorithm
            elif cfa_line[0] == "CFAGrid":
                hybrid_select_grid = cfa_line[1]
                hybrid_select_algorithm = algorithm
            elif cfa_line[0] == "CFAAlg":
                hybrid_select_grid = cfa_line[1]
                hybrid_select_algorithm = cfa_line[2]
            else:
                raise ValueError(cfa_line)
        cfa_0 = process_one(folder, global_grid, algorithm, γ)
        imageio.imsave(folder / 'cfa_0.png',
                       cfa_0)  # common for both cfa algorithms
        imageio.imsave(folder / 'cfa_grid_1.png', cfa_grid_1)
        cfa_alg_1 = process_one(folder, cfa_alg_grid, cfa_alg_alg, γ)
        imageio.imsave(folder / 'cfa_alg_1.png', cfa_alg_1)
        noise_0 = process_one(folder, global_grid, algorithm, γ, a0, b0)
        imageio.imsave(folder / 'noise_0.png', noise_0)
        noise_1 = process_one(folder, global_grid, algorithm, γ, a1, b1)
        imageio.imsave(folder / 'noise_1.png', noise_1)
        hybrid_select_0 = process_one(folder, global_grid, algorithm, γ,
                                      hybrid_select_noise_0_A,
                                      hybrid_select_noise_0_B)
        imageio.imsave(folder / 'hybrid_select_0.png', hybrid_select_0)
        hybrid_select_1 = process_one(folder, hybrid_select_grid,
                                      hybrid_select_algorithm, γ,
                                      hybrid_select_noise_1_A,
                                      hybrid_select_noise_1_B)
        imageio.imsave(folder / 'hybrid_select_1.png', hybrid_select_1)
