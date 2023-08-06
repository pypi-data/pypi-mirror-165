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
This file provides base class for all input forms defined by
the Coscine Python SDK.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from typing import TYPE_CHECKING, Union, MutableMapping, List, Tuple, Iterator
if TYPE_CHECKING:
	from .client import Client
	from .vocabulary import Vocabulary
from prettytable import PrettyTable
from datetime import datetime
from enum import Enum
from .exceptions import *
from .defaults import TIMEFORMAT, LANGUAGES

###############################################################################
# Class
###############################################################################

class FormField:
	"""
	The FormField class defines a field such as "Display Name"
	inside an InputForm with all of its properties.
	"""

	client: Client
	_data: dict

	def __init__(self, client: Client, data: dict) -> None:
		self.client = client
		self._data = data
	
	@property
	def name(self) -> str:
		return self._data["name"][LANGUAGES.index(self.client.language)]
	
	@property
	def path(self) -> str: return self._data["path"]

	@property
	def order(self) -> int: return int(self._data["order"])

	@property
	def vocabulary(self) -> str: return self._data["class"]

	@property
	def minCount(self) -> int: return int(self._data["minCount"])

	@property
	def maxCount(self) -> int: return int(self._data["maxCount"])

	@property
	def datatype(self) -> str: return self._data["datatype"]

###############################################################################
# Class
###############################################################################

class ValueFormat(Enum):
	"""
	Defines the value format

	Attributes
	-----------
	EXTERNAL
		The value format as apparent to the user (e.g. Informatik 409)
	INTERNAL
		The value format expected by Coscine (e.g. dict{diplayName: ...})
	UNIQUE
		Unique value identifier
	"""
	EXTERNAL = 0
	INTERNAL = 1
	UNIQUE = 2

###############################################################################
# Class
###############################################################################

class InputForm(MutableMapping):
	"""
	Coscine InputForm base class
	"""

	client: Client
	_items: List[FormField]
	_values: dict = {}
	_vocabularies: dict[str, Vocabulary] = {}

###############################################################################

	def __init__(self, client: Client) -> None:
		super().__init__()
		self.client = client

###############################################################################

	def __setitem__(self, key: str, value: object) -> None:
		self.set_value(key, value)

###############################################################################

	def __getitem__(self, key: str) -> Union(List, str):
		return self.get_value(key)

###############################################################################

	def __delitem__(self, key: str) -> None: del self._values[self.path(key)]

###############################################################################

	def __iter__(self) -> Iterator[str]: return iter(self.keys())

###############################################################################

	def __len__(self) -> int: return len(self._items)

###############################################################################

	def __str__(self) -> str: return self.str()

###############################################################################

	def clear(self) -> None:
		"""Remove all values of the InputForm"""
		self._values.clear()

###############################################################################

	def path(self, key: str) -> str:
		"""
		Returns the unique identifier for a multilanguage key.
		Logical example:
		path("Display Name") == path("Anzeigename") == "__XXX__"
		->> True
		where "__XXX__" is of some fixed internal value

		Parameters
		-----------
		key : str
			Multilanguage key
		"""
		return self.properties(key).path

###############################################################################

	def properties(self, key: str) -> FormField:
		"""
		Returns the form field properties corresponding to the given key.
		"""
		return self._items[self.index_of(key)]

###############################################################################

	def keys(self) -> List[str]:
		"""
		Returns a list of keys in their respective order based on the
		language setting of the client class instance used to initialize
		the InputForm.
		"""
		return [item.name for item in self._items]

###############################################################################

	def values(self, raw: bool = False) -> List[Union[str, List[str]]]:
		"""
		Returns a list of values in their respective order based on the
		language setting of the client class instance used to initialize
		the InputForm.

		Parameters
		----------
		raw : bool, default: False
			If set to true, values are not returned in a user-friendly
			format but instead in the actual language-independent format.
		"""
		return [self.get_value(key, raw) for key in self.keys()]

###############################################################################

	def items(self, raw: bool = False) -> List[Tuple[str, Union[str, List]]]:
		"""
		Returns a list of key, value pairs in their respective order based
		on the 	language setting of the client class instance
		used to initialize the InputForm.

		Parameters
		----------
		raw : bool, default: False
			If set to true, values are not returned in a user-friendly
			format but instead in the actual language-independent format.
		"""
		return zip(self.keys(), self.values(raw))

###############################################################################

	def is_valid(self, key: str, value: str, raw: bool = False) -> bool:
		"""
		Determines whether a given value for a key is valid based on
		the language setting of the client and if the value is part
		of a vocabulary in case of controlled fields.
		"""
		if self.is_required(key) and not value:
			raise ValueError(f"Expected value for required field {key}!")
		if not value: return True
		elif type(value) is not str and type(value) is not dict \
			 				and type(value) is not self.datatype(key):
			raise TypeError(
				f"Value set for key '{key}' is of invalid type:\n"\
				f"Expected str or {str(self.datatype(key))} but got "\
				f"{str(type(value))} instead."
			)
		if not self.is_controlled(key): return True
		else: return self.vocabulary(key).contains(value, raw)

###############################################################################

	def is_required(self, key: str) -> bool:
		"""
		Determines whether a key is a required one.
		"""
		return self.properties(key).minCount > 0

###############################################################################

	def is_controlled(self, key: str) -> bool:
		"""
		Determines whether a key is a controlled one.
		"""
		return self.properties(key).vocabulary is not None

###############################################################################

	def vocabulary(self, key: str) -> Vocabulary:
		"""
		Returns the vocabulary for the given key.
		"""
		if self.is_controlled(key):
			return self._vocabularies[self.path(key)]
		else:
			raise KeyError("Key is not controlled by a vocabulary!")

###############################################################################

	def index_of(self, key: str) -> int:
		"""
		Returns the order of the key.
		"""
		for index, item in enumerate(self.keys()):
			if item == key:
				return index
		raise KeyError(f"Key '{key}' not found in InputForm!")

###############################################################################

	def name_of(self, path: str) -> str:
		"""
		Returns the key name for the unique path
		"""
		for item in self._items:
			if item.path == path:
				return item.name
		raise KeyError(f"Path '{path}' not found!")

###############################################################################

	def datatype(self, key: str) -> type:
		"""
		Returns the datatype
		"""
		datatype = self.properties(key).datatype
		if datatype == "xsd:string":
			return str
		elif datatype == "xsd:boolean":
			return bool
		elif datatype == "xsd:date":
			return datetime
		else:
			return None

###############################################################################

	def is_typed(self, key: str) -> bool:
		"""
		Returns whether a value must have a certain datatype
		"""
		return self.datatype(key) is not None

###############################################################################

	def parse_value(self, key: str, value: object, reverse: bool = False) -> object:
		"""
		Converts a value to the datatype specified in its field.
		e.g. for a timestring "2022-01-01T10:12:00" returns a datetime object.
		"""

		if self.is_typed(key) and type(value) is str:
			if self.datatype(key) == datetime:
				return datetime.strptime(value, TIMEFORMAT)
		if self.is_controlled(key):
			value = self.vocabulary(key).lookup(value, reverse)

		return value

###############################################################################

	def add_value(self, key: str, value: object, raw: bool = False) -> None:
		if not self.is_valid(key, value, raw):
			raise ValueError(f"Invalid value for key '{key}': {value}")
		value = self.parse_value(key, value, raw)
		if not self.path(key) in self._values:
			self._values[self.path(key)] = [value]
		else:
			self._values[self.path(key)].append(value)

###############################################################################

	def set_value(self, key: str, value: object, raw: bool = False) -> None:
		if type(value) is list:
			for val in value:
				self.add_value(key, val, raw)
		else:
			if not self.is_valid(key, value, raw):
				raise ValueError(f"Invalid value for key '{key}': {value}")
			value = self.parse_value(key, value)
			self._values[self.path(key)] = [value]

###############################################################################

	def get_value(self, key: str, raw: bool = False) -> Union(List, str):
		path = self.path(key)
		if path in self._values:
			if self.is_controlled(key):
				if raw: return self._values[path]
				else: return [self.vocabulary(key).lookup(v, True) \
										for v in self._values[path]]
			else:
				return self._values[path]
		return []

###############################################################################

	def parse(self, data: dict) -> None:
		"""
		Parses data from Coscine into an InputForm.
		"""

###############################################################################

	def generate(self) -> dict:
		"""
		Generates Coscine formatted json-ld from an InputForm.
		"""

###############################################################################

	def value_str(self, key: str, raw: bool = False) -> str:
		"""
		Returns a value as a string
		"""
		string: str = ""
		values = self.get_value(key, raw)
		if len(values) > 1:
			string = "\n".join(values)
		elif len(values) == 1:
			string = values[0] if values[0] else ""
		return string

###############################################################################

	def str(self, format: str = "str", raw: bool = False) -> str:
		"""
		Returns a string in the specified format

		Parameters
		-----------
		format : str, default "str"
			Format of the string, possible options are: str, csv, json, html
		raw : bool, default False
			If set to true, values of the form are in Coscine internal format
		
		Returns
		--------
		str
		"""

		SUPPORTED_FORMATS = ["str", "csv", "json", "html"]
		if format not in SUPPORTED_FORMATS:
			raise ValueError(f"Unsupported format '{format}'!")
		table = PrettyTable(("C", "Property", "Value"), align="l")
		rows = []
		for key in self.keys():
			value = self.value_str(key, raw)
			name: str = key
			name = name + "*" if self.is_required(key) else name
			c: str = "X" if self.is_controlled(key) else ""
			rows.append((c, name, value))
		table.max_width["Value"] = 50
		table.add_rows(rows)
		if format == "str":
			return table.get_string()
		elif format == "csv":
			return table.get_csv_string()
		elif format == "json":
			return table.get_json_string()
		elif format == "html":
			return table.get_html_string()

###############################################################################