import imgaug as ia
from utils import Box
import numpy as np


class Augmenter:
    def __init__(self, seed=1):
        ia.seed(seed)
        self.seq = ia.augmenters.Sequential([
            ia.augmenters.Fliplr(0.5),
            ia.augmenters.Crop(percent=(0, 0.1)),
            ia.augmenters.Sometimes(0.5,
                                    ia.augmenters.GaussianBlur(sigma=(0, 0.5))
                                    ),
            ia.augmenters.ContrastNormalization((0.75, 1.5)),
            ia.augmenters.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
            ia.augmenters.Affine(
                scale={"x": (0.9, 1.1), "y": (0.9, 1.1)},
                translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)},
                rotate=(-25, 25),
                shear=(-4, 4)
            )
        ], random_order=True)

    def augment_image(self, image: np.ndarray, bounding_box: Box, label_is_present: bool):
        bbs = ia.BoundingBoxesOnImage(
            [ia.BoundingBox(
                x1=bounding_box.x1,
                y1=bounding_box.y1,
                x2=bounding_box.x2,
                y2=bounding_box.y2)],
            image.shape)

        bbs = bbs.clip_out_of_image()
        seq_det = self.seq.to_deterministic()
        aug_image = seq_det.augment_image(image=image)
        aug_bbs = seq_det.augment_bounding_boxes([bbs])[0]

        aug_bbs = aug_bbs.clip_out_of_image()

        aug_p = label_is_present #= label_is_present and aug_bbs.shape[0] > 0
        aug_coords = aug_bbs.bounding_boxes[0]

        return aug_image, \
               Box.from_points(x1=aug_coords.x1,
                               y1=aug_coords.y1,
                               x2=aug_coords.x2,
                               y2=aug_coords.y2), \
               aug_p
