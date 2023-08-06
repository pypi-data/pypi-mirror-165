__author__ = "Christian Stur"

from abc import ABC, abstractmethod
from pathlib import Path


from cbdf_api.interface import DATA_TYPES, PROBLEM_TYPES


class Preprocessor(ABC):
    """Use as a base class to write preprocessing steps for data. Each preprocessing file follows a template described
    in :ref:`developer_manual/custom_components/preprocessing:Structure of Preprocessing Files`. This component only
    receives input and output file locations to allow parallelization and resource efficient processing.
    """

    def __init__(self):
        self.data_types = DATA_TYPES
        self.problem_types = PROBLEM_TYPES

    @abstractmethod
    def get_preprocessor(self, data_in: Path, data_out: Path):
        """
        :param data_in: Filepath to the file to process.
        :type data_in: str
        :param data_out: Filepath to the file to save it to. Dont forget to save it!
        :type data_out: str
        :raises NotImplementedError: Your class needs to implement this method.
        """
        raise NotImplementedError
