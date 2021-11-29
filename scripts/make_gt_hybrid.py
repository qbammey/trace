#!/usr/bin/env python3
"""Create the ground truth for the Hybrid dataset"""

from pathlib import Path
import random

demosaicing_algorithms = ['LINEAR', 'VNG', 'PPG', 'AHD', 'DCB', 'DHT', 'AAHD']
n_demosaicing_algorithms = len(demosaicing_algorithms)
grids = ['RGGB', 'GRBG', 'GBRG', 'BGGR']
min_A = 0
max_A = 2
min_B = 0
max_B = 6
min_dist_A = 1
min_dist_B = 4
MIN_QUALITY = 75
MAX_QUALITY = 100


def obtain_samples(min_A, max_A, min_dist_A, min_B, max_B, min_dist_B):
    A_h = random.uniform(min_A + min_dist_A, max_A)
    B_h = random.uniform(min_B + min_dist_B, max_B)
    A_l = random.uniform(min_A, A_h - min_dist_A)
    B_l = random.uniform(min_B, B_h - min_dist_B)
    h = random.randint(0, 1)
    if h == 0:
        return A_h, B_h, A_l, B_l
    else:
        return A_l, B_l, A_h, B_h


if __name__ == "__main__":
    random.seed(0)
    folders = sorted(Path('../images/').glob('*'))
    for i_img, folder in enumerate(folders):
        print(i_img, end="\r")
        num_changes = random.randint(2, 3)
        exclude = None if num_changes == 3 else random.randint(
            0, 2)  # which to exclude if only 2 changes
        only_grids = random.random(
        ) < .5  # whether to change only CFA/JPEG grids, or algorithms and possibly grids (internal copy-move/splicing)
        with open(folder / 'gt_hybrid_select.txt', 'w') as f:
            if exclude != 0:  # noise
                noise_0_A, noise_0_B, noise_1_A, noise_1_B = obtain_samples(
                    min_A, max_A, min_dist_A, min_B, max_B, min_dist_B)
                f.write(
                    f'Noise {noise_0_A} {noise_0_B} {noise_1_A} {noise_1_B}\n')
            else:
                f.write('Noise None\n')
            if exclude != 1:  # jpeg
                if only_grids:
                    quality = random.randint(MIN_QUALITY, MAX_QUALITY)
                    δ_flat = random.randint(1, 63)
                    δy = δ_flat // 8
                    δx = δ_flat % 8
                    f.write(f'JPEGGrid {quality} {δy} {δx}\n')
                else:
                    quality_0 = random.randint(MIN_QUALITY, MAX_QUALITY)
                    quality_1 = quality_0
                    while quality_1 == quality_0:
                        quality_1 = random.randint(MIN_QUALITY, MAX_QUALITY)
                    δy, δx = random.randint(0, 7), random.randint(0, 7)
                    f.write(f'JPEGQual {quality_0} {quality_1} {δy} {δx}\n')
            else:
                f.write('JPEG None\n')
            if exclude != 2:  # CFA
                original_grid, original_algorithm, _ = open(
                    folder / 'gt_global.txt', 'r').readline().split()
                if only_grids:
                    new_grid = original_grid
                    while new_grid == original_grid:
                        new_grid = grids[random.randint(0, 3)]
                    f.write(f'CFAGrid {new_grid}\n')
                else:
                    new_grid = grids[random.randint(0, 3)]
                    new_algorithm = original_algorithm
                    while new_algorithm == original_algorithm:
                        new_algorithm = demosaicing_algorithms[random.randint(
                            0, n_demosaicing_algorithms - 1)]
                    f.write(f'CFAAlg {new_grid} {new_algorithm}\n')
            else:
                f.write('CFA None\n')
