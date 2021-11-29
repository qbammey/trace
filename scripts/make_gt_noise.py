#!/usr/bin/env python3
"""Create the ground truth for the Noise dataset."""
import random
from pathlib import Path

random.seed(0)

min_A = 0
max_A = 2
min_B = 0
max_B = 6
min_dist_A = 1
min_dist_B = 4

# Demosaic algorithm MODIFIED_AHD, AFD, VCD, VCD_MODIFIED_AHD,LMMSE, DHT, AAHD require GPL2 demosaic pack
# Demosaic algorithm AMAZE requires GPL3 demosaic pack


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
    for folder in folders:
        A_0, B_0, A_1, B_1 = obtain_samples(min_A, max_A, min_dist_A, min_B,
                                            max_B, min_dist_B)
        with open(folder / 'gt_noise.txt', 'w') as f:
            f.write(f'{A_0} {B_0}\n{A_1} {B_1}')
