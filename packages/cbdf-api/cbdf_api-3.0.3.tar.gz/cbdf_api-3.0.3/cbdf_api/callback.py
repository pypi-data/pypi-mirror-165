__author__ = "Christian Stur"

from abc import ABC, abstractmethod

from cbdf_api.interface import DATA_TYPES, PROBLEM_TYPES


class Callback(ABC):
    """To be implemented"""

    def __init__(self):
        self.data_types = DATA_TYPES
        self.problem_types = PROBLEM_TYPES

    @abstractmethod
    def get_callback(self):
        """
        :return: Returns a callback conforming to tensorflow.keras.callbacks.Callback
        :rtype: tensorflow.keras.callbacks.Callback
        :raises NotImplementedError: Your class needs to implement this method.
        """
        raise NotImplementedError
