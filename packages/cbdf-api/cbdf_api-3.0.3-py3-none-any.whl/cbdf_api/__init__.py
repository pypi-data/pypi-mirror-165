"""Top-level package for cbdf_api."""

import pkg_resources

__version__ = pkg_resources.get_distribution("cbdf_api").version

__author__ = """Christian Stur"""
__email__ = "christian.stur@aicura-medical.com"

from .architecture import Architecture
from .augmentation import Augmentation
from .callback import Callback
from .initializer import Initializer
from .loss import Loss
from .metric import Metric
from .optimizer import Optimizer
from .postprocessor import Postprocessor
from .preprocessor import Preprocessor
from .interface import *
from .interface import GlobalVariables as gv
from .generate_templates import gather_cbdf_api_objects
from .utils import *
