#!/usr/bin/env python3
from pathlib import Path
from tqdm import tqdm
from torch import max as tmax

import encoding

model = encoding.models.get_model('Encnet_ResNet50s_PContext',
                                  pretrained=True).cuda()
model.eval()


def process_one(path):
    img = encoding.utils.load_image(path / 'cfa_0.png').cuda().unsqueeze(0)
    output = model.evaluate(img)
    predict = tmax(output, 1)[1].cpu().numpy() + 1
    mask = encoding.utils.get_mask_pallete(predict, 'pascal_voc')
    mask.save(path / 'segmentation.png')


if __name__ == "__main__":
    folders = sorted(Path('../images/').glob('*'))
    tbar = tqdm(folders, leave=True, position=0, dynamic_ncols=True)
    for folder in tbar:
        tbar.write(folder.name)
        process_one(folder)
