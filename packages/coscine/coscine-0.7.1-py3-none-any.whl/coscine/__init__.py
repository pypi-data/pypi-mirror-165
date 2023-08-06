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
Coscine Python SDK

The Coscine Python SDK is an open source python package providing
a pythonic interface to the Coscine REST API. It is compatible
with Python versions 3.7+.

Please note that this python module is developed and maintained
by the scientific community and even though Copyright remains with
RWTH Aachen, it is not an official service that RWTH Aachen
provides support for.
"""

###############################################################################
# Dependencies
###############################################################################

from .config import Config
from .logger import Logger, LogLevel
from .exceptions import *
from .client import Client
from .project import Project, ProjectMember, ProjectForm
from .resource import Resource, ResourceForm
from .object import FileObject, MetadataForm
from .graph import ApplicationProfile

###############################################################################