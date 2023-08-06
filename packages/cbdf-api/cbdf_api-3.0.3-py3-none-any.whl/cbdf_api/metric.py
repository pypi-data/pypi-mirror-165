__author__ = "Christian Stur"

from abc import ABC, abstractmethod

from cbdf_api.interface import DATA_TYPES, PROBLEM_TYPES


class Metric(ABC):
    """The provided below metric functions are applied to estimate model performance. A list of tensorflow metrics are
    returned which are applied during training execution

    :return: An Aicura Metric Abstract Base Class.
    :rtype: Metric
    """

    def __init__(self):
        self.data_types = DATA_TYPES
        self.problem_types = PROBLEM_TYPES

    @abstractmethod
    def get_metric(self):
        """
        :return: list of tf.keras.metrics.Metric
        :rtype: list of tf.keras.metrics.Metric
        :raises NotImplementedError: Your class needs to implement this method.
        """
        raise NotImplementedError
