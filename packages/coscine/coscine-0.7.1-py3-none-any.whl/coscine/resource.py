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
This file defines the resource object for the representation of
Coscine resources. It provides an easy interface to interact with Coscine
resources from python.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from typing import TYPE_CHECKING, List, Callable
if TYPE_CHECKING:
	from .client import Client
	from .project import Project
from .exceptions import *
from .object import FileObject, MetadataForm
from .logger import ProgressBar
from .form import InputForm
from .graph import ApplicationProfile
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from prettytable.prettytable import PrettyTable
from concurrent.futures import ThreadPoolExecutor, wait
import json
import os

###############################################################################
# Class definition
###############################################################################

class S3info:
	"""
	Provides a simple pythonic interface to resource S3 access data
	"""

	read_access_key: str = ""
	read_secret_key: str = ""
	write_access_key: str = ""
	write_secret_key: str = ""
	endpoint: str = ""
	bucket: str = ""
	_data: dict

	def __init__(self, data: dict) -> None:
		self._data = data
		if "resourceTypeOption" in data and data["resourceTypeOption"]:
			opt: dict = data["resourceTypeOption"]
			self.read_access_key = opt.get("ReadAccessKey")
			self.read_secret_key = opt.get("ReadSecretKey")
			self.write_access_key = opt.get("WriteAccessKey")
			self.write_secret_key = opt.get("WriteSecretKey")
			self.endpoint = opt.get("Endpoint")
			self.bucket = opt.get("BucketName")

###############################################################################
# Class definition
###############################################################################

class ResourceForm(InputForm):
	"""
	"""

###############################################################################

	def __init__(self, client: Client) -> None:
		self._items = client.vocabularies.builtin("resource")
		super().__init__(client)
		vocabularies = {
			"type": client.vocabularies.resource_types(True),
			"applicationProfile": client.vocabularies.application_profiles(True),
			"license": client.vocabularies.licenses(True),
			"visibility": client.vocabularies.visibility(True),
			"disciplines": client.vocabularies.disciplines(True)
		}
		for item in self._items:
			if item.vocabulary:
				self._vocabularies[item.path] = vocabularies[item.path]

###############################################################################

	def parse(self, data: dict) -> None:
		IGNORE = ["id", "pid", "fixedValues", "creator", "archived"]
		if data is None:
			return
		for path, value in data.items():
			if path in IGNORE: continue
			key = self.name_of(path)
			self.set_value(key, value, True)

###############################################################################

	def generate(self) -> dict:
		metadata = {}

		# Collect missing required fields
		missing = []

		# Set metadata
		for key, values in self.items(True):
			
			if not values:
				if self.is_required(key):
					missing.append(key)
				continue

			properties = self.properties(key)
			metadata[properties.path] = values if len(values) > 1 else values[0]

		# Check for missing required fields
		if len(missing) > 0:
			if len(missing) == 1 and missing[0] == "resourceTypeOption" \
									and	metadata["type"] == "linked":
				pass
			else:
				raise ValueError(missing)

		return metadata

###############################################################################
# Class definition
###############################################################################

class Resource:
	"""
	Python representation of a Coscine Resource type.
	"""

	client: Client
	project: Project
	data: dict

	id: str
	pid: str
	name: str
	displayName: str
	type: str
	disciplines: List[str]
	profile: str
	archived: bool
	creator: str
	s3: S3info

###############################################################################

	def __init__(self, project: Project, data: dict) -> None:
		"""
		Initializes a Coscine resource object.

		Parameters
		----------
		project : Project
			Coscine project handle
		data : dict
			Resource data received from Coscine.
		"""

		self.project = project
		self.client = self.project.client
		self.data = data
		self.s3 = S3info(data)

###############################################################################

	@property
	def id(self) -> str: return self.data["id"]

	@property
	def pid(self) -> str: return self.data["pid"]

	@property
	def name(self) -> str: return self.data["resourceName"]

	@property
	def displayName(self) -> str: return self.data["displayName"]

	@property
	def license(self) -> str:
		return self.data["license"]["displayName"] \
			if self.data["license"] else ""

	@property
	def type(self) -> str: return self.data["type"]["displayName"]

	@property
	def disciplines(self) -> List[str]:
		lang = {
			"en": "displayNameEn",
			"de": "displayNameDe"
		}[self.client.language]
		return [k[lang] for k in self.data["disciplines"]]

	@property
	def profile(self) -> str: return self.data["applicationProfile"]

	@property
	def archived(self) -> bool: return bool(self.data["archived"])

	@property
	def creator(self) -> str: return self.data["creator"]

###############################################################################

	def __str__(self) -> str:
		table = PrettyTable(["Property", "Value"])
		rows = [
			("ID", self.id),
			("Resource Name", self.name),
			("Display Name", self.displayName),
			("PID", self.pid),
			("Type", self.type),
			("Disciplines", "\n".join(self.disciplines)),
			("License", self.license),
			("Application Profile", self.profile),
			("Archived", self.archived),
			("Creator", self.creator),
			("Project", self.project.displayName),
			("Project ID", self.project.id)
		]
		table.max_width["Value"] = 50
		table.add_rows(rows)
		return table.get_string(title = "Resource [%s]" % self.displayName)

###############################################################################

	def delete(self) -> None:
		"""
		Deletes the Coscine resource and all objects contained within it on
		the Coscine servers.
		"""

		uri = self.client.uri("Resources", "Resource", self.id)
		self.client.delete(uri)

###############################################################################

	def application_profile(self) -> ApplicationProfile:
		"""
		Returns the application profile of the resource
		"""

		return self.client.vocabularies.application_profile(self.profile)

###############################################################################

	def _download_concurrently(self, path: str = "./") -> None:
		with ThreadPoolExecutor(max_workers=4) as executor:
			files = self.objects()
			futures = [executor.submit(file.download, path) for file in files]
			wait(futures)
			for index, fut in enumerate(futures):
				try: fut.result()
				except CoscineException:
					self.client.logger.warn(
						f"Error downloading '{files[index].name}'.")

###############################################################################

	def download(self, path: str = "./", metadata: bool = False) -> None:
		"""
		Downloads the resource and all of its contents to the local harddrive.

		Parameters
		----------
		path : str, default: "./"
			Path to the local storage location.
		metadata : bool, default: False
			If enabled, resource metadata is downloaded and put in
			a hidden file '.metadata.json'.
		"""

		path = os.path.join(path, self.name)
		if not os.path.isdir(path):
			os.mkdir(path)
		if self.client.concurrent:
			self._download_concurrently(path)
		else:
			for file in self.objects():
				try: file.download(path)
				except CoscineException:
					self.client.logger.warn(f"Error downloading '{file.name}'.")
		if metadata:
			data = json.dumps(self.data, indent=4)
			fd = open(os.path.join(path, ".resource-metadata.json"), "w")
			fd.write(data)
			fd.close()

###############################################################################

	def objects(self, path: str = None, **kwargs) -> List[FileObject]:
		"""
		Returns a list of Objects stored within the resource

		Parameters
		------------
		kwargs
			file-object filter arguments (e.g. 'Name' = 'testfile').

		Returns
		-------
		list[Object]
			List of Coscine file-like objects.
		"""

		objects = []
		uri = self.client.uri("Tree", "Tree", self.id)
		if path:
			args = {"path": path}
		else:
			args = None
		data = self.client.get(uri, params = args).json()
		fileStorage = data["data"]["fileStorage"]
		metadataStorage = data["data"]["metadataStorage"]
		for data in fileStorage:
			for key, value in kwargs.items():
				if data[key] != value:
					break
			else:
				objects.append(FileObject(self, data))
		return objects

###############################################################################

	def object(self, path: str, **kwargs) -> FileObject:
		"""
		Returns an Object stored within the resource

		Parameters
		------------
		displayName : str, default: None
			file-object display name (filename/key).
		kwargs
			Filter

		Returns
		-------
		FileObject
			Python representation of the file-object as an Object instance
		"""
		
		objects = self.objects(path=path, **kwargs)
		if len(objects) == 1:
			return objects[0]
		elif len(objects) == 0:
			return None
		else:
			raise ValueError("Found more than 1 FileObject matching "\
											"the specified criteria!")

###############################################################################

	def upload(self, key: str, file, metadata = None, \
					callback: Callable[[int]] = None) -> None:
		"""
		Uploads a file-like object to a resource on the Coscine server

		Parameters
		----------
		key : str
			filename of the file-like object.
		file : object with read() attribute
				Either open file handle or local file location path.
		metadata : dict
			File metadata. For rds-s3 this is optional, but recommended.
		callback : Callable[int]
			Optional callback called during chunk uploads.
		"""

		if hasattr(file, "read"):
			fd = file
			filename = "MEM"
		elif type(file) is str:
			fd = open(file, "rb")
			filename = file
		else:
			raise TypeError("Argument `file` has unexpected type!")

		if metadata:
			if type(metadata) is MetadataForm:
				metadata = metadata.generate()
			uri = self.client.uri("Tree", "Tree", self.id, key)
			self.client.put(uri, data = metadata)

		uri = self.client.uri("Blob", "Blob", self.id, key)
		fields = {"files": (key, fd, "application/octect-stream")}
		encoder = MultipartEncoder(fields = fields)
		bar = ProgressBar(self.client.logger, encoder.len, filename, "UP", callback)
		monitor = MultipartEncoderMonitor(encoder, callback = \
				lambda monitor: bar.update(monitor.bytes_read - bar.n))
		headers = {"Content-Type": monitor.content_type}
		self.client.put(uri, data = monitor, headers = headers)

###############################################################################

	def set_archived(self, flag: bool) -> None:
		"""
		Set the archived flag of the resource to put it in read-only mode.
		Only the resource creator or project owner can do this.

		Parameters
		----------
		flag : bool
			Enable with True, Disable with False.
		"""

		uri = self.client.uri("Resources", "Resource", self.id, \
					"setReadonly?status=%s" % str(flag).lower())
		self.client.post(uri)
		self.data["archived"] = flag
		self.archived = flag

###############################################################################

	def form(self) -> ResourceForm:
		"""
		Returns a ResourceForm filled with the metadata of the current resource.

		Returns
		-------
		ResourceForm
		"""

		form = self.client.forms.resource()
		form.parse(self.data)
		return form

###############################################################################

	def update(self, form: ResourceForm) -> dict:
		"""
		Updates the metadata of the resource using the supplied ResourceForm.

		Parameters
		----------
		form : ResourceForm
			ResourceForm filled with updated values.
		"""

		if type(form) is ResourceForm:
			form = form.generate()
		elif type(form) is not dict:
			raise TypeError("")

		uri = self.client.uri("Resources", "Resource", self.id)
		response = self.client.post(uri, data = form)
		if response.ok: self.data = response.json()
		return response

###############################################################################

	def metadata(self, data: dict = None) -> MetadataForm:
		"""
		Creates a MetadataForm for this resource
		"""

		return self.client.forms.metadata(self.application_profile())

###############################################################################