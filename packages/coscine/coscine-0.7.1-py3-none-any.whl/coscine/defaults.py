###############################################################################
# Coscine Python SDK
# Copyright (c) 2018-2022 RWTH Aachen University
# Licensed under the terms of the MIT License
# #############################################################################
# Coscine, short for Collaborative Scientific Integration Environment is
# a platform for research data management (RDM).
# For more information on Coscine visit https://www.coscine.de/.
#
# Please note that this python module is open source software primarily
# developed and maintained by the scientific community. It is not
# an official service that RWTH Aachen provides support for.
###############################################################################

###############################################################################
# File description
###############################################################################

"""
This file defines default and constant data internally used by
multiple modules to avoid redefinitions.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from typing import List
from appdirs import AppDirs
from .__about__ import __version__

###############################################################################

# The time format for parsing Coscine date strings with datetime
TIMEFORMAT: str = "%Y-%m-%dT%H:%M:%S"

# Build default application directory paths
APPDIR: AppDirs = AppDirs("coscine-python-sdk", "Coscine")

# The name for the persistent cache file storage
CACHEFILE: str = f"{__version__}-cache.json"

# The languages supported by the Coscine Python SDK
LANGUAGES: List[str] = ["de", "en"]

# Supported formats for printing forms
TABLE_FORMATS: List[str] = ["str", "csv", "json", "html"]

###############################################################################