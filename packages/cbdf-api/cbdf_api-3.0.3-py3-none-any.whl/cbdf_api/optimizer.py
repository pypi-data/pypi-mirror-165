__author__ = "Christian Stur"

from abc import ABC, abstractmethod

from cbdf_api.interface import DATA_TYPES, PROBLEM_TYPES


class Optimizer(ABC):
    """An optimizer detailed in the optimizer tensorflow class.

    :return: An Aicura Optimizer Abstract Base Class.
    :rtype: Optimizer
    """

    def __init__(self):
        self.data_types = DATA_TYPES
        self.problem_types = PROBLEM_TYPES

    @abstractmethod
    def get_optimizer(self):
        """
        :return: Returns an optimzer object
        :rtype: tensorflow.keras.optimizers.Optimizer
        :raises NotImplementedError: Your class needs to implement this method.
        """
        raise NotImplementedError
