#!/usr/bin/env python3
"""Create the ground truth for the CFA Grid and CFA Algorithm datasets."""

from pathlib import Path
import random

demosaicing_algorithms = ['LINEAR', 'VNG', 'PPG', 'AHD', 'DCB', 'DHT', 'AAHD']
n_demosaicing_algorithms = len(demosaicing_algorithms)
grids = ['RGGB', 'GRBG', 'GBRG', 'BGGR']

if __name__ == "__main__":
    random.seed(0)
    folders = sorted(Path('../images/').glob('*'))
    for folder in folders:
        original_grid, original_algorithm, _ = open(folder / 'gt_global.txt',
                                                    'r').readline().split()
        new_grid = original_grid
        while new_grid == original_grid:
            new_grid = grids[random.randint(0, 3)]
        open(folder / 'gt_cfa_grid.txt', 'w').write(new_grid)
        new_grid = grids[random.randint(0, 3)]
        new_algorithm = original_algorithm
        while new_algorithm == original_algorithm:
            new_algorithm = demosaicing_algorithms[random.randint(
                0, n_demosaicing_algorithms - 1)]
        open(folder / 'gt_cfa_algorithm.txt',
             'w').write(f'{new_grid} {new_algorithm}')
