__author__ = "Christian Stur"

from abc import ABC, abstractmethod

from cbdf_api.interface import DATA_TYPES, PROBLEM_TYPES


class Initializer(ABC):
    """Choose an Initializer to prime a network with a set of weights previous to training.

    :return: An Aicura Initializer Abstract Base Class.
    :rtype: Initializer
    """

    def __init__(self):
        self.data_types = DATA_TYPES
        self.problem_types = PROBLEM_TYPES

    @abstractmethod
    def get_initializer(self):
        """
        :return: Returns a tensorflow initializer
        :rtype: tensorflow.initializers.Initializer
        :raises NotImplementedError: Your class needs to implement this method.
        """
        raise NotImplementedError
