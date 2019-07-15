import os
from utils.project_managment import PROJECT_ROOT


MODEL_PATH = f"{PROJECT_ROOT}/tests/resources/yolo/yolo_test_model"
LINK = "https://mega.nz/#!Nah3GIQC!JHg98pU_HpZoFxMHmChzyayqMJRIeYFTUf-3vX64gWk"
IMG_PATH = f"{PROJECT_ROOT}/tests/resources/yolo/img.png"
IMG_LINK = "https://mega.nz/#!UCpXkChT!CIflbL91dPaKgmNx1Zqd35oQC8js_YJsunKULFDcZUY"


def prepare_test_yolo():
    """
    Utility function for downloading example Yolo pretrained model with example image for testing
    :return: None
    """

    if not os.path.isdir(MODEL_PATH):
        print("Model not found, downloading from google drive...")
        os.system(f"cd {PROJECT_ROOT}/tests/resources/yolo && megatools dl '{LINK}'")

        if not os.path.isfile(f"{MODEL_PATH}.zip"):
            print("Error: Could not download model file, aborting...")
            exit(-1)

        os.system(f"cd {PROJECT_ROOT}/tests/resources/yolo && unzip {MODEL_PATH}.zip && rm {MODEL_PATH}.zip")

        if not os.path.isdir(MODEL_PATH):
            print("Error occured while unziping test model archive, aborting...")
            exit(-2)
    else:
        print("Model file already downloaded. I will use it")

    if not os.path.isfile(IMG_LINK):
        print("Example image not found, downloading from google drive")
        os.system(f"cd {PROJECT_ROOT}/tests/resources/yolo && megatools dl '{IMG_LINK}'")

        if not os.path.isfile(f"{IMG_PATH}"):
            print("Error: Could not download example image file, aborting...")
            exit(-3)

    print("Downloaded test yolo model sucessfully")