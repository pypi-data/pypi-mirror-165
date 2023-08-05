import json
import logging
import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from monai.transforms import LoadImage
from ruamel.yaml import YAML

log = logging.getLogger(__name__)


def make_if_dont_exist(folder_path, overwrite=False):
    """
    creates a folder if it does not exists
    input:
    folder_path : relative path of the folder which needs to be created
    over_write :(default: False) if True overwrite the existing folder
    """
    if os.path.exists(folder_path):

        if not overwrite:
            log.info(f"{folder_path} exists.")
        else:
            log.info(f"{folder_path} overwritten.")
            shutil.rmtree(folder_path)
            os.makedirs(folder_path)

    else:
        os.makedirs(folder_path)
        log.info(f"{folder_path} created!")


def read_yaml(yaml_path):
    """
    Reads .yaml file and returns a dictionary
    """
    yaml_path = Path(yaml_path)
    yaml = YAML(typ="safe")
    data = yaml.load(yaml_path)
    return data


def save_yaml(data, yaml_path):
    """
    Saves a dictionary to .yaml file
    """
    yaml_path = Path(yaml_path)
    yaml = YAML(typ="safe")
    yaml.dump(data, yaml_path)


def load_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data


def save_json(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)


def load_image(img_path) -> np.ndarray:
    img = LoadImage()(img_path)
    return img[0]


def save_predictions_to_csv(y_true, y_pred, output_path):
    predictions = pd.DataFrame(
        {"y_true": y_true, "y_pred_proba": y_pred}
    ).sort_values("y_true", ascending=False)
    predictions.to_csv(output_path, index=False)
