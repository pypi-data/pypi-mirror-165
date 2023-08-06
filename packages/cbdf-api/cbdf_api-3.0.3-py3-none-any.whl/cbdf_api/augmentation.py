__author__ = "Amal Bouchrit"

from abc import ABC, abstractmethod

from cbdf_api.interface import DATA_TYPES, PROBLEM_TYPES
from typing import Dict, List


class Augmentation(ABC):
    """Choose a method to artificially expand the size of a training set or modify training examples from the existing
    ones. The augmentations are applied during training time.

    :return: An Aicura Augmentation Abstract Base Class.
    :rtype: Augmentation
    """

    def __init__(self):
        self.data_types = DATA_TYPES
        self.problem_types = PROBLEM_TYPES

    @abstractmethod
    def get_augmentation(self, data: Dict[str, List]) -> Dict[str, List]:
        """
        :param data: A dictionary containg the keys 'inputs' containing a list of x variables and 'target' containing
            the y variables.
        :type inputs: Dict[str, List]

        :return: Returns the augmented data as a dictionary with the associate keys 'inputs' and 'target' as received
            in the input
        :rtype: Dict[str, List]
        :raises NotImplementedError: Your class needs to implement this method.
        """
        raise NotImplementedError
