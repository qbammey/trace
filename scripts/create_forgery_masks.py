#!/usr/bin/env python

from pathlib import Path
import random

import numpy as np
import imageio
from skimage import measure
from skimage.transform import resize

# requires an even number of images
root_path = Path('../images/')
image_paths = list(
    map(lambda x: x.parent, root_path.glob('*/segmentation.png')))
n_images = len(image_paths)

masks = []
sizes = []

random.seed(0)
for path in image_paths:
    seg = imageio.imread(path / 'segmentation.png')[:, :, :3]
    Y, X, _ = seg.shape
    done_mask = False
    studied = np.zeros((Y, X), bool)
    while not done_mask:
        y = random.randint(0, Y - 1)
        x = random.randint(0, X - 1)
        if studied[y, x]:
            continue
        big_mask = np.product(
            seg == seg[y, x][None, None],
            axis=-1)  # This mask may contain multiple components.
        labels = measure.label(big_mask, background=0)
        final_mask = labels == labels[
            y, x]  # This mask only has one connected component.
        size = np.count_nonzero(final_mask) / (Y * X)
        if size <= 0.5:
            masks.append(final_mask)
            sizes.append(size)
            imageio.imsave(path / 'mask_endo.png',
                           255 * final_mask.astype(np.uint8))
            done_mask = True
        else:
            studied += final_mask
    print(path, end="\r")

size_order = np.argsort(sizes)


def pair(k):
    return k - k % 2 + (k + 1) % 2


for i_size in range(
        n_images
):  # i_size represents the size rank we're currently processing
    i_image = size_order[
        i_size]  # i_image represents the id of the image for which we create a mask
    image_path = image_paths[i_image]
    i_mask = size_order[pair(
        i_size
    )]  # i_mask represents the id of the mask we'll use, which is paired with i_image
    Y_img, X_img = imageio.imread(image_path / 'cfa_0.png').shape[:2]
    mask = masks[i_mask]
    Y_mask, X_mask = mask.shape
    if (Y_img, X_img) != (Y_mask, X_mask):
        mask = resize(mask, (Y_img, X_img))
    mask = 255 * mask.astype(np.uint8)
    imageio.imsave(image_path / 'mask_exo.png', mask)
