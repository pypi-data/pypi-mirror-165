__author__ = "Christian Stur"

from abc import ABC, abstractmethod

from cbdf_api.interface import DATA_TYPES, PROBLEM_TYPES


class Architecture(ABC):
    """AICURA medical offers architectures integrated into the CBDF. Below is a list and description for each of the
    models grouped by machine learning task. To adjust the components and write your own components. For this you can
    find a detailed description at :ref:`developer_manual/custom_components/architecture:Structure of Architecture
    Files`. Parameters for example the 3D ResNet can be specified as follows in the 'Component Framework' section
    of your App.

    .. code-block::

        "architectures": {
            "resnet_3D": {
                "block_type": ' ',
                "repetitions": []
            }
        }

    :param input_shape: The input dimensionality of the data. If provided and set to the Input part of the tensorflow
        model it will dynamically assigned based on the shape of the data after preprocessing, defaults to None
    :type input_shape: tuple, optional

    :return: An Aicura Architecture Abstract Base Class.
    :rtype: Architecture
    """

    def __init__(self):
        self.data_types = DATA_TYPES
        self.problem_types = PROBLEM_TYPES

    @abstractmethod
    def get_architecture(self):
        """
        :return: Returns a tensorflow uncompiled model
        :rtype: tensorflow.keras.Model
        :raises NotImplementedError: Your class needs to implement this method.
        """
        raise NotImplementedError
