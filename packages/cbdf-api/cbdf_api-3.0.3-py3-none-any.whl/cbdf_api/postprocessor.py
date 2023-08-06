__author__ = "Christian Stur"

from abc import ABC, abstractmethod

from cbdf_api.interface import DATA_TYPES, PROBLEM_TYPES
from typing import Dict, List, Any


class Postprocessor(ABC):
    """Postprocessing step allows to organise the output data in a desirable format. To create a new postprocessing
    component, please refer to the following page
    :ref:`developer_manual/custom_components/postprocessing:Structure of Postprocessing Files`. For example, the class
    mapper can be specified in config section of the app_defs.json file as follows. The received input is organized as
    the expected output. Example:
    [
        {
            "identifier": "Peter_Fox123"
            "prediction" : [0.0, 0.8, 0.2]
        },
        {
            "identifier": "Mimi_Valet281"
            "prediction" : [0.1, 0.2, 0.7]
        },
    ]

    .. code-block::

        "postprocessing": {
            "class_mapper": {
                "my_variable": 3
            }
        }
    """

    def __init__(self):
        self.data_types = DATA_TYPES
        self.problem_types = PROBLEM_TYPES

    @abstractmethod
    def get_postprocessor(self, output: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """

        :param output: As described above
        :type output: List[Dict[str, Any]]
        :raises NotImplementedError: Your class needs to implement this method.
        :return: As described above
        :rtype: List[Dict[str, Any]]
        """
        raise NotImplementedError
