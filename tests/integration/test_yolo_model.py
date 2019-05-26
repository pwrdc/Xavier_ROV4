import unittest
from neural_networks.YoloServer.YoloModel import YoloModel
import os
import cv2


class TestYoloModel(unittest.TestCase):

    MODEL_PATH = "yolo_test_model"
    LINK = "https://mega.nz/#!Nah3GIQC!JHg98pU_HpZoFxMHmChzyayqMJRIeYFTUf-3vX64gWk"
    IMG_PATH = "img.png"
    IMG_LINK = "https://mega.nz/#!UCpXkChT!CIflbL91dPaKgmNx1Zqd35oQC8js_YJsunKULFDcZUY"

    def setUp(self) -> None:
        if not os.path.isdir(self.MODEL_PATH):
            print ("Model not found, downloading from google drive")
            os.system(f"megadl '{self.LINK}")

            if not os.path.isfile(f"{self.MODEL_PATH}.zip"):
                print("Error: Could not download model file, aborting...")
                exit(-1)

            os.system(f"unzip {self.MODEL_PATH}.zip && rm {self.MODEL_PATH}.zip")

            if not os.path.isdir(self.MODEL_PATH):
                print("Error occured while unziping test model archive, aborting...")
                exit(-2)
        else:
            print("Model file already downloaded. I will use it")

        if not os.path.isdir(self.MODEL_PATH):
            print("Example image not found, downloading from google drive")
            os.system(f"megadl '{self.IMG_LINK}")

            if not os.path.isfile(f"{self.IMG_PATH}"):
                print("Error: Could not download example image file, aborting...")
                exit(-3)

        print("Setup ok")

    def test_ModelSetup(self):
        img = cv2.imread(self.IMG_PATH)
        model = YoloModel(self.MODEL_PATH)
        model.load()
        print(model.predict(img))


if __name__ == '__main__':
    unittest.main()