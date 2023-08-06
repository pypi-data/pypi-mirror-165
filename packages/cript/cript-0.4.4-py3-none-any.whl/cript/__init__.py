import logging
import pkg_resources

import pint


# Set the default logging level for the package
logging.basicConfig(level=logging.WARNING)
logging.captureWarnings(True)
pint.util.logger.setLevel(logging.ERROR)  # Mute Pint warnings

# Single-sourcing the package version
version_file = pkg_resources.resource_filename("cript", "VERSION.txt")
with open(version_file, "r") as fr:
    __version__ = fr.read().strip()

VERSION = __version__
__short_version__ = __version__.rpartition(".")[0]


# Instantiate the Pint unit registry
# https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects
# Note that this needs to be before the node imports below
pint_ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)


from cript import exceptions  # noqa 401 402
from cript.nodes import (  # noqa 402
    User,
    Group,
    Project,
    Reference,
    Citation,
    Collection,
    File,
    Data,
    Condition,
    Property,
    Identifier,
    Material,
    Inventory,
    Quantity,
    Ingredient,
    Equipment,
    Process,
    Experiment,
)

NODE_CLASSES = [
    User,
    Group,
    Project,
    Reference,
    Citation,
    Collection,
    File,
    Data,
    Condition,
    Property,
    Identifier,
    Material,
    Inventory,
    Quantity,
    Ingredient,
    Equipment,
    Process,
    Experiment,
]

from cript.api import API  # noqa 401 402
