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
Implements classes and routines for manipulating Metadata and interacting
with files and file-like data in Coscine.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from typing import TYPE_CHECKING, List, Callable
if TYPE_CHECKING:
	from .client import Client
	from .resource import Resource
from .defaults import TABLE_FORMATS
from .exceptions import *
from .logger import ProgressBar
from .graph import ApplicationProfile
from .form import InputForm, FormField
from .utils import HumanBytes
from prettytable.prettytable import PrettyTable
import os

###############################################################################
# Class definition
###############################################################################

class MetadataForm(InputForm):
	"""
	The MetadataForm supports parsing coscine.Object metadata, generating
	metadata and manipulating it in the same way one would manipulate
	a python dict.
	"""

	profile: ApplicationProfile

###############################################################################

	def __init__(self, client: Client, graph: ApplicationProfile) -> None:
		"""
		Initializes an instance of type MetadataForm.

		Parameters
		----------
		client : Client
			Coscine Python SDK client handle
		graph : str
			Coscine application profile rdf graph as json-ld string
		"""

		self.profile = graph
		super().__init__(client)
		self._items = [FormField(client, item) for item in self.profile.items()]
		# Query vocabularies for controlled fields
		for item in self._items:
			if item.vocabulary:
				self._vocabularies[item.path] = \
					client.vocabularies.instance(item.vocabulary)

###############################################################################

	def generate(self) -> dict:
		"""
		Generates and validates metadata for sending to Coscine.
		"""

		metadata = {}

		metadata[ApplicationProfile.RDFTYPE] = [{
			"type": "uri",
			"value": self.profile.target()
		}]

		# Collect missing required fields
		missing = []

		# Set metadata
		for key, values in self.items(True):
			
			if not values:
				if self.is_required(key):
					missing.append(key)
				continue

			properties = self.properties(key)
			metadata[properties.path] = []
			for value in values:
				entry = {
					"value": value,
					"datatype": properties.datatype \
						if properties.datatype else properties.vocabulary,
					"type": "uri" if properties.vocabulary else "literal"
				}
				if not entry["datatype"]:
					del entry["datatype"]
				metadata[properties.path].append(entry)

		# Check for missing required fields
		if len(missing) > 0:
			raise ValueError(missing)

		return metadata

###############################################################################

	def parse(self, data: dict) -> None:
		if data is None:
			return
		for path, values in data.items():
			if path == ApplicationProfile.RDFTYPE:
				continue
			key = self.name_of(path)
			self.set_value(key, [v["value"] for v in values], True)

###############################################################################
# Class definition
###############################################################################

class FileObject:
	"""
	Objects in Coscine represent file-like data. We could have called it
	'File', but in case of linked data we are not actually dealing with files
	themselves, but with links to files.Thus we require a more general
	datatype.
	"""

	client: Client
	resource: Resource
	data: dict

	name: str
	size: int
	type: str
	path: str
	is_folder: bool

	@property
	def name(self) -> str: return self.data["Name"]

	@property
	def size(self) -> int: return int(self.data["Size"])

	@property
	def type(self) -> str: return self.data["Kind"]

	@property
	def filetype(self) -> str:
		return os.path.splitext(self.data["Name"])[1]

	@property
	def path(self) -> str: return self.data["Path"]

	@property
	def is_folder(self) -> bool: return bool(self.data["IsFolder"])

	CHUNK_SIZE: int = 4096

###############################################################################

	def __init__(self, resource: Resource, data: dict) -> None:
		"""
		Initializes the Coscine FileObject.

		Parameters
		----------
		resource : Resource
			Coscine resource handle.
		data : dict
			data of the file-like object.
		"""

		# Configuration
		self.client = resource.client
		self.resource = resource
		self.data = data

###############################################################################

	def __str__(self) -> str: return self.str()

###############################################################################

	def str(self, format: str = "str") -> str:
		"""
		Returns a string in the specified format

		Parameters
		-----------
		format : str, default "str"
			Format of the string, possible options are: str, csv, json, html

		Returns
		--------
		str
		"""

		if format not in TABLE_FORMATS:
			raise ValueError(f"Unsupported format '{format}'!")

		table = PrettyTable(("Property", "Value"))
		rows = [
			("Name", self.name),
			("Size", HumanBytes.format(self.size)),
			("Type", self.type),
			("Path", self.path),
			("Folder", self.is_folder)
		]
		table.max_width["Value"] = 50
		table.add_rows(rows)
		if format == "str":
			return table.get_string(title = "Object [%s]" % self.name)
		elif format == "csv":
			return table.get_csv_string(title = "Object [%s]" % self.name)
		elif format == "json":
			return table.get_json_string(title = "Object [%s]" % self.name)
		elif format == "html":
			return table.get_html_string(title = "Object [%s]" % self.name)

###############################################################################

	def metadata(self) -> dict:
		"""
		Retrieves the metadata of the file-like object.

		Returns
		-------
		dict
			Metadata as a python dictionary.
		None
			If no metadata has been set for the file-like object.
		"""

		uri = self.client.uri("Tree", "Tree", self.resource.id)
		args = {"path": self.path}
		data = self.client.get(uri, params=args).json()
		metadata = data["data"]["metadataStorage"]
		if not metadata:
			return None
		metadata = metadata[0]
		for key in metadata:
			return metadata[key]

###############################################################################

	def update(self, metadata) -> None:
		"""
		Updates the metadata of the file-like object.

		Parameters
		----------
		metadata : MetadataForm or dict
			MetadataForm or JSON-LD formatted metadata dict
		
		Raises
		------
		TypeError
			If argument `metadata` has an unexpected type.
		"""

		if type(metadata) is MetadataForm:
			metadata = metadata.generate()
		elif type(metadata) is not dict:
			raise TypeError("Expected MetadataForm or dict.")
		
		uri = self.client.uri("Tree", "Tree", self.resource.id)
		args = {"path": self.path}
		self.client.put(uri, params = args, data = metadata)

###############################################################################

	def content(self) -> bytes:
		"""
		Retrieves the content/data of the object. In case of linked data
		this would be the link, not the actual file itself. It is impossible
		to get the file contents of linked data objects with this python module.
		In case of rds or rds-s3 data this would return the file contents.
		Be aware that for very large files this will consume a considerable
		amount of RAM!

		Returns
		-------
		bytes
			A raw byte-array containing the Coscine file-object's data.
		"""

		uri = self.client.uri("Blob", "Blob", self.resource.id)
		args = {"path": self.path}
		return self.client.get(uri, params = args).content

###############################################################################

	def download(self, path: str = "./", callback: Callable[[int]] = None) -> None:
		"""
		Downloads the file-like object to the local harddrive.

		Parameters
		----------
		path : str, default: "./"
			The path to the download location on the harddrive.
		callback : function(chunksize: int)
			A callback function to be called during downloading chunks.
		"""

		uri = self.client.uri("Blob", "Blob", self.resource.id)
		args = {"path": self.path}
		response = self.client.get(uri, params = args, stream = True)
		path = os.path.join(path, self.name)
		fd = open(path, "wb")
		bar = ProgressBar(self.client.logger, self.size, self.name, "DOWN", callback)
		for chunk in response.iter_content(chunk_size = self.CHUNK_SIZE):
			fd.write(chunk)
			bar.update(len(chunk))
		fd.close()

###############################################################################

	def delete(self) -> None:
		"""
		Deletes the file-like object on the Coscine server.
		"""

		uri = self.client.uri("Blob", "Blob", self.resource.id)
		args = {"path": self.path}
		self.client.delete(uri, params = args)

###############################################################################

	def objects(self, **kwargs) -> List[FileObject]:
		if self.is_folder:
			return self.resource.objects(path=self.path, **kwargs)
		else:
			raise TypeError("object is not a directory!")

###############################################################################

	def object(self, displayName: str = None, **kwargs) -> FileObject:
		if self.is_folder:
			if displayName.endswith("/"): # expect directory
				displayName = self.name + "/" + displayName
			return self.resource.object(displayName = displayName,
											path=self.path, **kwargs)
		else:
			raise TypeError("object is not a directory!")

###############################################################################

	def form(self) -> MetadataForm:
		"""
		Returns a MetadataForm to interact with the metadata of the FileObject.
		"""

		graph = self.resource.application_profile()
		form = MetadataForm(self.client, graph)
		form.parse(self.metadata())
		return form

###############################################################################

	def move(self, resource: Resource) -> None:
		"""
		Move a file-like object to another resource
		"""
		resource.upload(self.name, self.content(), self.metadata())

###############################################################################