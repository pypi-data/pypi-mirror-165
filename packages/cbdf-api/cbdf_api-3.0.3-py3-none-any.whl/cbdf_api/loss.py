__author__ = "Christian Stur"

from abc import ABC

from cbdf_api.interface import DATA_TYPES, PROBLEM_TYPES


class Loss(ABC):
    """AICURA Advanced functionality provides custom made loss functions which can be used in optimization problems for
    classification, regression and segmentation tasks.

    :return: An Aicura Loss Abstract Base Class.
    :rtype: Loss
    """

    def __init__(self):
        self.data_types = DATA_TYPES
        self.problem_types = PROBLEM_TYPES

    def get_loss(self):
        """
        :return: Returns a tensorflow losses function
        :rtype: tensorflow.keras.losses
        :raises NotImplementedError: Your class needs to implement this method.
        """
        raise NotImplementedError
