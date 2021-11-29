#!/usr/bin/env python3
"""Create the ground truth for parameters shared between datasets: gamma correction, main demosaicing algorithm and mosaic grid"""

from pathlib import Path
import random

demosaicing_algorithms = ['LINEAR', 'VNG', 'PPG', 'AHD', 'DCB', 'DHT', 'AAHD']
n_demosaicing_algorithms = len(demosaicing_algorithms)
grids = ['RGGB', 'GRBG', 'GBRG', 'BGGR']
γ_min = 1
γ_max = 2.5

if __name__ == "__main__":
    random.seed(0)
    folders = sorted(Path('../images/').glob('*'))
    for folder in folders:
        alg = demosaicing_algorithms[random.randint(
            0, n_demosaicing_algorithms - 1)]
        grid = grids[random.randint(1, 3)]
        γ = random.uniform(γ_min, γ_max)
        with open(folder / 'gt_global.txt', 'w') as f:
            f.write(f'{grid} {alg} {γ}')
