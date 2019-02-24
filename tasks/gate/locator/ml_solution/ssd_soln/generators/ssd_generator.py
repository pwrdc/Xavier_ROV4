import os
import tables
import numpy as np
import pandas as pd
import cv2
from utils import Box
from net_parameters import S_MIN, S_MAX, FEATURE_MAPS
from generators.augmenter import Augmenter
from generators.label_assigning import generate_labels
from generators.visualisation import show_bounding_boxes


class TrainImageGenerator:
    batch_size = 10

    def __init__(self):
        self.annotations_path = "../unity_data/annotations.csv"
        self.images_path = "../unity_data"
        self.input_image_width = 300
        self.input_image_height = 300
        self.batch_size = 32
        self.augmenter = Augmenter(32)

        self.annotations_table = None
        self.num_samples = None
        self.num_batches = None

        if not os.path.exists(self.annotations_path):
            raise RuntimeError(f"Couldn't find annotation file in location {self.annotations_path}")

        if not os.path.exists(self.annotations_path):
            raise RuntimeError(f"Couldn't find image folder in location {self.images_path}")

        self._load_annotations()

        if len(self.annotations_table) == 0:
            raise RuntimeError(f"No annotations found in file {self.annotations_path}")

    def _load_annotations(self):
        self.annotations_table = pd.read_csv(self.annotations_path)
        self.num_samples = len(self.annotations_table)
        self.num_batches = self.num_samples // self.batch_size

    def _generate_sample(self, index):
        image_path = f'{self.images_path}/{self.annotations_table["file"][index]}'
        x = self.annotations_table["x"][index]
        y = self.annotations_table["y"][index]
        w = self.annotations_table["w"][index]
        h = self.annotations_table["h"][index]
        p = self.annotations_table["p"][index]

        image = cv2.imread(image_path)
        img_c = image
        bounding_box = Box(x, y, w, h)

        image, bounding_box, p = self.augmenter.augment_image(image, bounding_box, p)
        image = image / 255.0
        bounding_box = bounding_box.normalize(image.shape[1], image.shape[0])
        image = cv2.resize(image, (self.input_image_width, self.input_image_height))
        label = generate_labels(bounding_box, FEATURE_MAPS)

        # Uncomment to visualise input
        #show_bounding_boxes(image, label, with_corrections=True)

        return image, label

    def _generate_batch(self, indexes):
        batch_x = []
        batch_y = []

        for i in indexes:
            x,y = self._generate_sample(i)

            batch_x.append(x)
            batch_y.append(y)

        return batch_x, batch_y

    def _generate_to_file(self, path: str):
        pass


if __name__ == "__main__":
    gen = TrainImageGenerator()

    gen.generate_batch([0, 1,2,3])
