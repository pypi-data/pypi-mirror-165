__author__ = "Christian Stur"

import argparse
import importlib
import inspect
import json
import os
import shutil
from typing import Any, Dict, List
from pathlib import Path
import pkg_resources

from cbdf_api.architecture import Architecture
from cbdf_api.augmentation import Augmentation
from cbdf_api.callback import Callback
from cbdf_api.initializer import Initializer
from cbdf_api.loss import Loss
from cbdf_api.metric import Metric
from cbdf_api.optimizer import Optimizer
from cbdf_api.postprocessor import Postprocessor
from cbdf_api.preprocessor import Preprocessor

API_CLASSES = [
    Architecture,
    Augmentation,
    Callback,
    Initializer,
    Loss,
    Metric,
    Optimizer,
    Postprocessor,
    Preprocessor,
]
allowed_types = [int, float, str, list, dict, bool]


class SimpleEncoder(json.JSONEncoder):
    """Removes not standard python data types"""

    def default(self, obj: Any):
        if not any([isinstance(obj, a_type) for a_type in allowed_types]):
            result = None
        else:
            result = obj

        return result


def get_arguments():
    """Parses input arguments.

    :return: Input arguments
    :rtype:
    """
    parser = argparse.ArgumentParser(
        description="Component Based Development Framework to create pipelines for your machine learning project"
    )

    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="./",
        help="Specify the directory in which the template files are saved.",
    )
    parser.add_argument(
        "-a",
        "--append",
        action="store_true",
        help="If the template_advanced.json inside the given output_dir should be appended instead of overwritten.",
    )
    parser.add_argument(
        "package",
        type=str,
        help="Specify the package name for which you want to create the app templates (Needs to be installed)",
    )

    args = parser.parse_args()

    return args


def gather_cbdf_api_objects(module_name: str, template_advanced=None) -> dict:
    """Imports given a module until confronted with a non-module and given the assumption it to be a class, hand it to
    fill entries to add it to the template. The given module name has to be installed.

    :param module: The name of a module.
    :type module: str
    :param template_advanced: The advanced template for UI selection of Components.
    :type template_advanced: dict
    :return: The advanced template for UI selection of Components.
    :rtype: dict
    """
    if template_advanced is None:
        template_advanced = get_empty_config()

    try:
        a_module = importlib.import_module(module_name)
        full_names = get_full_object_names(a_module)
        for names in full_names:
            template_advanced = gather_cbdf_api_objects(names, template_advanced)
    except ModuleNotFoundError:
        module_name, class_object = ".".join(module_name.split(".")[:-1]), module_name.split(".")[-1]
        a_module = importlib.import_module(module_name)
        my_object = getattr(a_module, class_object)

        if inspect.isclass(my_object):
            if any([issubclass(my_object, supercomp) and my_object != supercomp for supercomp in API_CLASSES]):
                template_advanced = fill_entries(my_object, template_advanced)

    return template_advanced


def get_empty_config() -> Dict[str, Dict]:
    """
    :return: Returns an empty template for the advanced template.
    :rtype: Dict[str, Dict]
    """
    config = {
        "init": {"architectures": {}, "initializers": {}},
        "train": {
            "preprocessors": {},
            "augmentations": {},
            "metrics": {},
            "losses": {},
            "optimizers": {},
            "callbacks": {},
        },
        "predict": {"preprocessors": {}, "postprocessors": {}},
        "test": {},
        "vars": {"epochs": 1},
    }

    return config


def get_full_object_names(module) -> List[str]:
    """Gets all names of objects in a module

    :param module: _description_
    :type module: _type_
    :return: List of full paths to the given module.
    :rtype: List[str]
    """
    names = module.__all__ if hasattr(module, "__all__") else dir(module)
    names = [name for name in names if not name.startswith("_")]
    full_names = [".".join([module.__name__, n]) for n in names]

    return full_names


def fill_entries(obj, template_advanced: dict) -> dict:
    """Routes based on the object type the entry to the correct level in the template

    :return: The advanced template for UI selection of Components.
    :rtype: dict
    """

    if issubclass(obj, Architecture):
        template_advanced = add_entry(obj, "init", "architectures", template_advanced)
    elif issubclass(obj, Initializer):
        template_advanced = add_entry(obj, "init", "initializers", template_advanced)
    elif issubclass(obj, Augmentation):
        template_advanced = add_entry(obj, "train", "augmentations", template_advanced)
    elif issubclass(obj, Callback):
        template_advanced = add_entry(obj, "train", "callbacks", template_advanced)
    elif issubclass(obj, Loss):
        template_advanced = add_entry(obj, "train", "losses", template_advanced)
    elif issubclass(obj, Metric):
        template_advanced = add_entry(obj, "train", "metrics", template_advanced)
    elif issubclass(obj, Optimizer):
        template_advanced = add_entry(obj, "train", "optimizers", template_advanced)
    elif issubclass(obj, Postprocessor):
        template_advanced = add_entry(obj, "predict", "postprocessors", template_advanced)
    elif issubclass(obj, Preprocessor):
        template_advanced = add_entry(obj, "train", "preprocessors", template_advanced)
        template_advanced = add_entry(obj, "predict", "preprocessors", template_advanced)

    return template_advanced


def add_entry(obj, mode: str, component_type: str, template_advanced: dict) -> dict:
    """Adds a singular entry to the advanced template, while removing duplicate entries in preference for shorter
    entries

    :param mode: One of the following modes: ["init", "train", "predict"]
    :type mode: str
    :param component_type: The entry level to which the component will be added in the template_advanced.
    :type component_type: str
    :param obj: The object which is a candidate for the advanced template.
    :type obj: object
    :param template_advanced: The advanced template for UI selection of Components.
    :type template_advanced: dict
    :return: The advanced template for UI selection of Components.
    :rtype: dict
    """

    defaults = get_object_defaults(obj)
    template_advanced[mode][component_type][get_object_path(obj)] = defaults
    template_advanced = deduplicate_entries(obj, mode, component_type, template_advanced)

    return template_advanced


def get_object_defaults(obj) -> Dict[str, Any]:
    """Retrieves the default values for an Object.

    :param obj: An instantiated Object.
    :type obj: _type_
    :return: A Dictionary with the names of the variables as key and their default value as value.
    :rtype: Dict[str, Any]
    """
    obj_specs = inspect.getfullargspec(obj)
    if len(obj_specs.args) > 1:
        defaults = {str(k): v for k, v in zip(obj_specs.args[1:], list(obj_specs.defaults))}
        defaults.update({"data_types": obj().data_types, "problem_types": obj().problem_types})
    else:
        defaults = {}

    return defaults


def get_object_path(obj) -> str:
    """
    :param obj: An instantiated Object.
    :type obj: _type_
    :return: The path leading from the module level to the Object level joined by '.'
    :rtype: str
    """
    return ".".join(obj.__module__.split(".")[:-1]) + f".{obj.__name__}"


def deduplicate_entries(obj, mode: str, component_type: str, template_advanced: dict) -> dict:
    """Deduplicates entries based on double representations of import paths. If multiple entries are found, the shorter
    ones are kept and the others removed.

    :param obj: _description_
    :type obj: _type_
    :param mode: _description_
    :type mode: str
    :param component_type: _description_
    :type component_type: str
    :param template_advanced: _description_
    :type template_advanced: dict
    :return: _description_
    :rtype: dict
    """
    potentially_same = [i for i in template_advanced[mode][component_type].keys() if i.endswith(obj.__name__)]

    for other_path in potentially_same:
        module_name, class_object = ".".join(other_path.split(".")[:-1]), other_path.split(".")[-1]
        a_module = importlib.import_module(module_name)
        other_obj = getattr(a_module, class_object)
        if obj == other_obj:
            path = get_object_path(obj)
            if len(other_path) > len(path):
                template_advanced[mode][component_type].pop(other_path)
            elif len(other_path) < len(path):
                template_advanced[mode][component_type].pop(path)
            else:
                pass

    return template_advanced


def save_templates(template_advanced: dict, output_dir: Path):
    """Saves the template_advanced.json and template_recommend.

    :param template_advanced: The advanced template for UI selection of Components.
    :type template_advanced: dict
    """
    template_advanced_out_fp = os.path.join(output_dir, "template_advanced.json")
    template_recommend_in_fp = pkg_resources.resource_filename("cbdf_api", "dist/template_recommend.json")
    template_recommed_out_fp = os.path.join(output_dir, "template_recommend.json")

    print(f"Saving {template_advanced_out_fp}")
    with open(template_advanced_out_fp, "w") as outfile:
        json.dump(template_advanced, outfile, indent=4, cls=SimpleEncoder)

    print(f"Saving {template_recommed_out_fp}")
    shutil.copyfile(template_recommend_in_fp, template_recommed_out_fp)


def main():
    """Generates the template_advanced.json and template_recommended.json for the UI to select components and assign
    variables. Exampl usage: 'python generate_template_advanced.py --output_dir ../dist --package my_package --append'
    """
    args = get_arguments()

    if getattr(args, "append"):
        original_fp = os.path.join(getattr(args, "output_dir"), "template_advanced.json")
        with open(original_fp, "r") as fin:
            template_advanced = json.load(fin)
    else:
        template_advanced = None

    template_advanced = gather_cbdf_api_objects(
        module_name=getattr(args, "package"), template_advanced=template_advanced
    )

    save_templates(template_advanced=template_advanced, output_dir=getattr(args, "output_dir"))


if __name__ == "__main__":
    main()
