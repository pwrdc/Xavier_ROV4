import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '4' 
from utils.project_managment import PROJECT_ROOT
import argparse
from pathlib import Path
from glob import glob
from os import mkdir

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.FATAL)

if __name__ == "__main__":  
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Path to unstripped model. Eg ~/models/modelYOLO_path/model.chkpt")
    parser.add_argument("-o", "--output", required=True, help="Path to output stripped model. Eg ~/models_stripped/modelYOLO_path/model.chkpt")

    args = parser.parse_args()

    input_model = args.input
    output_model = args.output

    session = tf.Session()
    saver = tf.train.import_meta_graph(f"{input_model}.meta")

    graph = tf.get_default_graph()

    tf.graph_util.extract_sub_graph()

    saver.restore(session, input_model)

    if not Path(output_model).parent.is_dir():
        mkdir(Path(output_model).parent.as_posix())

    print(f"Saving to {output_model}")
    saver2 = tf.train.Saver(tf.trainable_variables())
    saver2.save(session, output_model)

