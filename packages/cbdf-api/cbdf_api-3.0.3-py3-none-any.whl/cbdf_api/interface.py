__author__ = "Christian Stur"

import os
import json
import logging
from typing import List
import sys


MODES = ["init", "train", "predict", "test", None]
DATA_TYPES = ["image", "tabular", "text", "time_series"]
PROBLEM_TYPES = [
    "single-label_classification",
    "multi-label_classification",
    "detection",
    "regression",
    "segmentation",
    "data_exploration",
]
ENTRY_TEMPLATE = {
    "fhirName": "test",
    "value_type": "int",
    "table": "patient",
    "input_value": [],
    "categories": 0,
    "sequence": False,
    "requires_value": False,
    "x": False,
    "y": False,
    "filtering": False,
}


class Singleton(type):
    """Abstract class that internally allows only a single instance of itsself to be created."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class GlobalVariables(metaclass=Singleton):
    """A global singleton class carrying during runtime all relevant configurations selected via the UI, current mode
    (e.g 'init', 'train', 'predict'), the Logger, and all directory info. model.h5 is located in the MODEL_IN_DIR, the
    input.json in the DATA_IN_DIR.

    :param metaclass: _description_, defaults to Singleton
    :type metaclass: _type_, optional
    :return: _description_
    :rtype: _type_
    """

    ROOT_DIR: str = "/"
    CONFIG: dict
    APP_DEFS: dict
    LOGGER: logging.Logger
    LOCAL: bool
    MODE: str
    DATA_IN_DIR: str
    DATA_OUT_DIR: str
    MODEL_IN_DIR: str
    MODEL_OUT_DIR: str
    TEMP_DIR: str
    MONITORING_DIR: str
    COMP_DIR: str
    TRAIN_X_IDS: List[str]
    TRAIN_Y_IDS: List[str]
    TRAIN_IDS: List[str]
    PREDICT_X_IDS: List[str]
    PREDICT_OUTPUT_IDS: List[str]
    CURRENT_X_IDS: List[str]
    CURRENT_MODE_IDS: List[str]
    ALL_IDS: List[str]
    CONTINUOUS_IDS: List[str]
    CATEGORICAL_IDS: List[str]
    DEPENDENT_ID: str
    DIAGNOSES_IDS: List[str]
    ALL_DATA: object

    def __init__(self):
        pass

    def configure(self, root_dir: str = "/", mode: str = "init", local: bool = False):
        assert os.path.exists(root_dir), f"{root_dir} does not exist"
        assert mode in MODES, f"Mode {mode} is not supported, please choose one of {MODES}"

        self.ROOT_DIR = root_dir
        self.MODE = mode
        self.LOCAL = local

        self.set_paths()
        self.initialize_logger()

    def set_paths(self):
        self.DATA_IN_DIR = os.path.join(self.ROOT_DIR, "data_in")
        self.DATA_OUT_DIR = os.path.join(self.ROOT_DIR, "data_out")
        self.MODEL_IN_DIR = os.path.join(self.ROOT_DIR, "model")
        self.TEMP_DIR = os.path.join(self.ROOT_DIR, "temp")
        self.MONITORING_DIR = os.path.join(self.DATA_OUT_DIR, "monitoring")
        self.COMP_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

        if self.LOCAL:
            self.MODEL_OUT_DIR = self.MODEL_IN_DIR
        else:
            self.MODEL_OUT_DIR = os.path.join(self.DATA_OUT_DIR, "model")

    def initialize_logger(self):
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(self.TEMP_DIR, "pipeline.log"),
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            format="%(levelname)s: %(message)-60s (%(module)s.%(funcName)s)",
        )
        self.LOGGER = logging.getLogger("cbdf_logger")
        self.LOGGER.addHandler(logging.StreamHandler(sys.stdout))

    def init_folder_structure(self):
        os.makedirs(os.path.join(self.ROOT_DIR, "app"), exist_ok=True)
        os.makedirs(os.path.join(self.ROOT_DIR, "app", "config"), exist_ok=True)
        os.makedirs(self.DATA_IN_DIR, exist_ok=True)
        os.makedirs(self.DATA_OUT_DIR, exist_ok=True)
        os.makedirs(self.TEMP_DIR, exist_ok=True)
        os.makedirs(self.MODEL_IN_DIR, exist_ok=True)
        os.makedirs(self.MODEL_OUT_DIR, exist_ok=True)
        os.makedirs(self.MONITORING_DIR, exist_ok=True)

    # app_defs modifications/readings
    def load_app_defs(self):
        self.APP_DEFS = self.get_latest_app_defs()
        self.CONFIG = self.APP_DEFS["config"][0]

        self.load_ids()

    def get_latest_app_defs(self, latest: bool = True) -> dict:
        """
        :param latest: If the latest processed version of the app_defs should be returned, defaults to True
        :type latest: bool, optional
        :return: Provides the dictionary of the app_defs.json
        :rtype: dict
        """
        app_defs_fp = os.path.join(self.ROOT_DIR, "app", "config", "app_defs.json")
        processed_app_defs_fp = os.path.join(self.TEMP_DIR, "processed_app_defs.json")

        try:
            if os.path.exists(processed_app_defs_fp) and latest:
                filepath = processed_app_defs_fp
            else:
                filepath = app_defs_fp

            with open(filepath, encoding="utf-8") as fin:
                my_app_defs = json.load(fin)

            return my_app_defs

        except FileNotFoundError:
            self.LOGGER.info(
                f"Didn't find app_defs.json "
                f"in {os.path.dirname(app_defs_fp)}: {os.listdir(os.path.dirname(app_defs_fp))}."
            )

    def load_ids(self):
        """Reloads all entries present in APP_DEFS["inputs"] and APP_DEFS["predictonInputs"] and assignes them to the
        according variable name.
        """
        self.TRAIN_X_IDS = [i["fhirName"] for i in self.APP_DEFS["inputs"] if i["x"] is True]
        self.TRAIN_Y_IDS = [i["fhirName"] for i in self.APP_DEFS["inputs"] if i["y"] is True]
        self.TRAIN_IDS = self._deduplicate(self.TRAIN_X_IDS + self.TRAIN_Y_IDS)

        self.PREDICT_X_IDS = [i["fhirName"] for i in self.APP_DEFS["predictionInputs"] if i["x"] is True]

        self.CURRENT_X_IDS = self.TRAIN_X_IDS if self.MODE == "train" else self.PREDICT_X_IDS
        self.CURRENT_MODE_IDS = self.TRAIN_IDS if self.MODE == "train" else self.PREDICT_X_IDS

        self.ALL_IDS = self._deduplicate(self.CURRENT_X_IDS)

    def _deduplicate(self, a_list: list) -> list:
        return list(set(a_list))

    def save_processed_app_defs(self):
        with open(os.path.join(self.TEMP_DIR, "processed_app_defs.json"), "w") as fout:
            json.dump(self.APP_DEFS, fout, indent=4)

    def clear_input_output_list(self, list_key: str = None, entry_keys: list = None):
        """Deletes entries from the input/output list and saves it in the processed_app_defs.json file.

        :param list_key: If specified only deletes the entry from the provided list. Possible list_keys are "inputs",
            "predictionInputs". When None specified it deleted from all lists, defaults to None
        :type list_key: str, optional
        :param entry_keys: A list of fhirNames by which it should kick them out, defaults to None
        :type entry_keys: list, optional
        """
        if list_key:
            self.APP_DEFS[list_key] = [d for d in self.APP_DEFS[list_key] if d["fhirName"] not in entry_keys]
            self.save_processed_app_defs()
            self.load_app_defs()
        else:
            self.clear_input_output_list("inputs", entry_keys)
            self.clear_input_output_list("predictionInputs", entry_keys)

    def add_entry_input_output_list(self, list_key: str = None, kwargs: dict = {"fhirName": "test"}):
        """Adds a default empty entry to the input/output list and saves it in the processed_app_defs.json file. With
        **kwargs the internal values can be set

        :param list_key: If specified only adds the entry to the provided list. Possible list_keys are "inputs",
            "predictionInputs". When None specified it deleted from all lists, defaults to None
        :type list_key: str, optional
        :param kwargs: A dictionary containing values , defaults to {"fhirName":"test"}
        """
        entry = ENTRY_TEMPLATE.copy()
        entry = {k: (v if k not in kwargs else kwargs[k]) for k, v in entry.items()}

        if list_key:
            if entry not in self.APP_DEFS[list_key]:
                self.APP_DEFS[list_key].append(entry)
            self.save_processed_app_defs()
            self.load_app_defs()
        else:
            self.add_entry_input_output_list("inputs", kwargs)
            self.add_entry_input_output_list("predictionInputs", kwargs)

    def get_entire_id_entry(self, fhirName: str, list_key: str = None) -> dict:
        """Returns the entire entry as defined in the APP_DEFS for the provided fhirName.

        :param fhirName: [description]
        :type fhirName: str
        :return: [description]
        :rtype: dict
        """
        if list_key is None:
            if self.MODE == "train":
                list_key = "inputs"
            else:
                list_key = "predictionInputs"

        entry = [entry for entry in self.APP_DEFS[list_key] if entry["fhirName"] == fhirName][0]

        return entry

    def get_batch_size(self, data_set: str) -> int:
        """Returns the batch size"""
        testing: bool = self.CONFIG["vars"].get("testing", False)
        if testing:
            return 1
        elif data_set == "train":
            return self.APP_DEFS["trainingBatchSize"]
        elif data_set == "val":
            return self.APP_DEFS["validationSetSize"]
        elif data_set == "predict":
            return self.APP_DEFS["predictionBatchSize"]

    # Path information
    def get_latest_input_file_path(self, latest: bool = True) -> str:
        """
        :param latest: If the latest processed version of the input.json should be returned, defaults to True
        :type latest: bool, optional
        :return: Provides filepath to latest version of the input.json
        :rtype: str
        """
        input_json_fp = os.path.join(self.DATA_IN_DIR, "input.json")
        processed_json_fp = os.path.join(self.TEMP_DIR, "processed_input.json")

        try:
            if os.path.exists(processed_json_fp) and latest:
                filepath = processed_json_fp
            else:
                filepath = input_json_fp

            return filepath

        except FileNotFoundError:
            self.LOGGER.info(
                f"Didn't find input.json "
                f"in {os.path.dirname(input_json_fp)}: {os.listdir(os.path.dirname(input_json_fp))}."
            )


class CBDFException(Exception):
    """Template Exception for CBDF"""


class UnsupportedOptionException(CBDFException):
    """The given variabe does not fit any of the possible options"""


class NotYetDefinedException(CBDFException):
    """The part to be executed is planned but not yet implemented/available"""


class UnpreferableException(CBDFException):
    """The given configuration is unpreferable but possible. Might lead to skipping behaviour"""


class ShouldNeverGetHereException(CBDFException):
    """If this Exception is raised a case happened that should not. Please contact IT for further details"""
