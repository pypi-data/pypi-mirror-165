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
This file implements a basic persistent cache for nonvolatile Coscine
data such as metadata vocabularies.
The data is automatically refreshed every once in a while.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from .__about__ import __version__
from .defaults import APPDIR, CACHEFILE, TIMEFORMAT
import atexit
import json
import os
from json.decoder import JSONDecodeError
from datetime import datetime, timedelta

###############################################################################
# Class
###############################################################################

class Cache:
	"""
	A basic persistent cache for temporary storage of nonvolatile data.
	Data is automatically refreshed when it exceeds a certain age.
	Data is loaded from & stored on disk if persistency option is enabled.

	Attributes
	-----------
	_cache : dict
		A simple dictionary to store the cached data.
	_persistent : bool
		Controls cache persistence - if enabled the cache is saved to
		a file and restored upon the next session.
	"""

	_cache: dict
	_persistent: bool

###############################################################################

	def __init__(self, persistent: bool = True) -> None:
		"""
		Initializes a Cache instance and attempts to load a previous
		cache copy from a file if the $persistent option is set.

		Parameters
		----------
		persistent : bool
			Enable to save the cache in a file upon program exit and
			to restore it in the next session.
		"""

		self._persistent = persistent
		self.load()

###############################################################################

	def save(self) -> None:
		"""
		Saves the current session cache into a file if
		the $persistent option is set (see __init__()).
		Any cachefile existing prior is overwritten.
		"""

		if self._persistent and self._cache:
			path = APPDIR.user_cache_dir
			if not os.path.exists(path):
				os.makedirs(path, exist_ok=True)
			filepath = os.path.join(path, CACHEFILE)
			fd = open(filepath, "w")
			fd.write(json.dumps(self._cache))
			fd.close()

###############################################################################

	def load(self) -> None:
		"""
		Loads a previously stored session cache for use with the
		current session. If no previous session is found, the cache
		is intialized as an empty dict.
		"""

		if self._persistent:
			atexit.register(self.save)
			try:
				path = APPDIR.user_cache_dir
				filepath = os.path.join(path, CACHEFILE)
				fd = open(filepath, "r")
				self._cache = json.loads(fd.read())
				fd.close()
			except (FileNotFoundError, JSONDecodeError):
				self._cache = {}
		else:
			self._cache = {}

###############################################################################

	def get(self, key: str) -> str:
		"""
		Attempts to read a cached dataset from the cache via a key.

		Parameters
		----------
		key : str
			The key used to save data in the cache (e.g. a URL)
		
		Returns
		--------
		str
			The cached data for the given key
		None
			If the key is not present in the cache or if the data is
			likely to be outdated
		"""

		if key in self._cache:
			lastTime = datetime.strptime(self._cache[key]["time"], TIMEFORMAT)
			if ((datetime.now() - lastTime) < timedelta(days=24)):
				return self._cache[key]["data"]
		return None

###############################################################################

	def set(self, key: str, data) -> None:
		"""
		Sets data inside the cache via a key. If that key is already
		present any data referenced by it is overwritten.

		Parameters
		----------
		key : str
			The key used for saving data in the cache (e.g. a URL)
		"""

		self._cache[key] = {
			"time": datetime.now().strftime(TIMEFORMAT),
			"data": data
		}

###############################################################################

	def clear(self) -> None:
		"""
		Clears the cache
		"""

		self._cache.clear()

###############################################################################