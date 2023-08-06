import json
from tqdm import tqdm
import os
from typing import Dict, List
from cbdf_api import gv


class JsonPbar:
    def __init__(self, description: str):
        self.description = description
        self.pbar = tqdm(desc=self.description)

    def pbar_hook(self, obj):
        patient = obj.get("identifier")

        if patient:
            self.update()

        return obj

    def update(self):
        self.pbar.update()


def load_original_input_json() -> List[Dict]:
    """When requiring the original unaltered data (before preprocessing), request such by this function.

    :return: A list of patients represented by a dictionary
    :rtype: List[Dict]
    """
    with open(os.path.join(gv().DATA_IN_DIR, "input.json"), "r") as fin:
        data = json.load(fin)

    return data


def load_json(filepath: str):
    """Wrapper to simply load json files.

    :param filepath: Filepath to the file to load
    :type filepath: str
    :return: A json file read
    :rtype: parsed json_file
    """
    try:
        verbose = gv().CONFIG["vars"].get("verbose", 2)
    except:
        verbose = 2

    if verbose == 1:
        with open(filepath, "r") as fin:
            return json.load(fin, object_hook=JsonPbar(description=f"Loading {os.path.basename(filepath)}").pbar_hook)
    else:
        with open(filepath, "r") as fin:
            return json.load(fin)


def save_json(obj: dict, filepath: str, encoder: json.JSONEncoder = None):
    """Wrapper to simply save json files.

    :param filepath: Filepath to the file to save to
    :type filepath: str
    :param encoder: Additional ecoder applied to the json to be saved to.
    :type encoder: json.JSONEncoder, defaults to None
    """
    try:
        verbose = gv().CONFIG["vars"].get("verbose", 2)
    except:
        verbose = 2

    if verbose == 1:
        gv().LOGGER.info(f"Saving {os.path.basename(filepath)}")

    with open(filepath, "w") as fout:
        if encoder is not None:
            json.dump(obj, fout, indent=4, cls=encoder)
        else:
            json.dump(obj, fout, indent=4)
