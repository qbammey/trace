# Non-Semantic Evaluation of Image Forensics Tools: Methodology and Database
Quentin Bammey, Tina Nikoukhah, Marina Gardella, Rafael Grompone von Gioi, Miguel Colom, Jean-Michel Morel
Centre Borelli — École Normale Supérieure Paris-Saclay — Université Paris-Saclay

## Abstract
We propose a new method to evaluate image forensics tools, that characterizes what image cues are being used by each detector. Our method enables effortless creation of an arbitrarily large dataset of carefully tampered images in which controlled detection cues are present. Starting with raw images, we alter aspects of the image formation pipeline inside a mask, while leaving the rest of the image intact. This does not change the image's interpretation; we thus call such alterations non-semantic, as they yield no semantic inconsistencies.
This method avoids the painful and often biased creation of convincing semantics.
All aspects of image formation (noise, CFA, compression pattern and quality, etc.\@) can vary independently in both the authentic and tampered parts of the image.
Alteration of a specific cue enables precise evaluation of the many forgery detectors that rely on this cue, and of the sensitivity of more generic forensic tools to each specific trace of forgery, and can be used to guide the combination of different methods.
Based on this methodology, we create a database and conduct an evaluation of the main state-of-the-art image forensics tools, where we characterize the performance of each method with respect to each detection cue.

## Database
The dataset can be accessed [here](http://boucantrin.ovh.hw.ipol.im/static/quentin/trace.zip).

## Code
The provided code can create new forgeries in the same way that they were created in the article. `generate_database.sh` will run all the scripts in order.

### Structure
To run the provided code, original images should be placed in the `images/` directory. Each image should be in its own subdirectory under the name `original.NEF`. For instance, an image could be placed at `images/foo/original.NEF`.

1. `make_gt_global.py`, `make_gt_noise.py`, `make_gt_cfa.py`, `make_gt_jpeg.py`, `make_gt_hybrid.py` will generate parameters for both processing pipelines in the different datasets.
2. `process_nef.py` will generate the two images in each dataset.
3. `segment.py` can be used to create segmentation maps of the images, then `create_forgery_masks.py` will select a random region of each image to create the endomask and use the same region on another image as exomask. Depending on the nature of the images, other segmentation methods may be better suited.
4. Finally, `merge_images.py` will use the generated images and forgery masks to merge two images into one forgery.


## License
The Trace forgery images database is derived from authentic images of the [RAISE dataset](http://loki.disi.unitn.it/RAISE).
Following policy of the RAISE dataset, it is thus to be used only for non-commercial research and educational purposes.

If using the dataset in any published work, please cite both the Trace article (full citation to come once the article is published):
Q. Bammey, T. Nikoukhah, M. Gardella, R. Grompone von Gioi, M. Colom, J.-M. Morel, Non-Semantic Evaluation of Image Forensics Tools: Methodology and Database, Winter Conference on Applications of Computer Vision, Waikoloa, Hawaii, 2022

and the RAISE dataset article from where the images are derived:
.-T. Dang-Nguyen, C. Pasquini, V. Conotter, G. Boato, RAISE – A Raw Images Dataset for Digital Image Forensics, ACM Multimedia Systems, Portland, Oregon, March 18-20, 2015
```
@inproceedings{dang2015raise,
  title={Raise: A raw images dataset for digital image forensics},
  author={Dang-Nguyen, Duc-Tien and Pasquini, Cecilia and Conotter, Valentina and Boato, Giulia},
  booktitle={Proceedings of the 6th ACM multimedia systems conference},
  pages={219--224},
  year={2015}
}
```
