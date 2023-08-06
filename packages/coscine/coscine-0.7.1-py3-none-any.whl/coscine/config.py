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
This file provides an easy way of reading coscine-python-sdk
config files.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from .__about__ import __version__
from .defaults import APPDIR
import json
import os

###############################################################################
# Class
###############################################################################

class Config:
	"""
	A class to read from coscine-python-sdk config files.
	Lookup order:  
		0. Custom path specified in constructor (fail if not found)  
		1. Local config file  
		2. Local config directory  
		3. System directory (e.g. User/AppData/Local/... on Windows)  
	"""

	token: str = None
	language: str = None
	concurrent: bool = True

###############################################################################

	def __init__(self, path: str = "") -> None:
		"""
		Initialized the configuration file interface with an
		optional path argument.
		
		Parameters
		-----------
		path : str
			If set to a valid file path, an attempt is made to laod
			the file referenced by path as a config.
		
		Raises
		-------
		FileNotFoundError
			In case no config file could have been located.
		"""

		if path:
			self.load(path)
		elif os.path.exists(".config.json"):
			self.load(".config.json")
		elif os.path.exists(".coscine/"):
			self.load(os.path.join(".coscine/", "config.json"))
		elif os.path.exists(APPDIR.user_config_dir):
			self.load(os.path.join(APPDIR.user_config_dir, "config.json"))
		else:
			raise FileNotFoundError("Failed to locate config file!")

###############################################################################

	def load(self, path: str) -> None:
		"""
		Loads a valid coscine-python-sdk config file and validates
		the file for correctness.

		Parameters
		-----------
		path : str
			The filepath to the configuration file (must include filename)
		"""

		fd = open(path, "r")
		data = json.load(fd)
		fd.close()
		self.token = data["token"] if "token" in data else None
		self.language = data["language"] if "language" in data else None
		self.concurrent = data["concurrent"] if "concurrent" in data else True

###############################################################################