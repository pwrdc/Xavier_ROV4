import os
from os import mkdir, system
from utils.project_managment import PROJECT_ROOT
import argparse
from pathlib import Path
from glob import glob


if __name__ == "__main__":  
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Path to folder containg unstripped models in subfolders")
    parser.add_argument("-o", "--output", required=True, help="Path to folder where stripped models will be stored")
    parser.add_argument("-n", "--name", default="model.chkpt", help="Models name, eg. model.chkpt")

    args = parser.parse_args()

    input_folder = Path(args.input)
    output_folder = Path(args.output)
    model_name = args.name

    for model in input_folder.glob("*"):
        if model.is_dir():
            output_directory = output_folder / model.name

            if not output_directory.is_dir():
                mkdir(output_directory.as_posix())

            system(f"python3 -m scripts.strip_model -i {model.as_posix()}/{model_name} -o {output_directory.as_posix()}/{model_name}")

    print("All done :)")




