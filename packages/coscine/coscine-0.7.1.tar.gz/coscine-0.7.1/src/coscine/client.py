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
This file contains the backbone of the Coscine Python SDK - the client class.
The client class acts as the manager of the SDK and is mainly
responsible for the communication and exchange of information 
with Coscine servers.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from typing import List
import sys
import json
from json.decoder import JSONDecodeError
import requests
import urllib.parse
from .logger import Logger
from .cache import Cache
from .vocabulary import VocabularyManager
from .graph import ApplicationProfile
from .project import Project, ProjectForm
from .resource import ResourceForm
from .object import FileObject, MetadataForm
from .__about__ import __version__
from .defaults import LANGUAGES
from .exceptions import *

###############################################################################
# Class
###############################################################################

class FormManager:
	"""
	Serves empty InputForms
	"""

	client: Client

	def __init__(self, client: Client) -> None:
		self.client = client
	def metadata(self, graph: ApplicationProfile) -> MetadataForm:
		"""
		Generates a metadata form
		"""
		return MetadataForm(self.client, graph)
	def project(self, parent: Project = None) -> ProjectForm:
		"""
		Generates a project form
		"""
		return ProjectForm(self.client, parent)
	def resource(self) -> ResourceForm:
		"""
		Generates a resource form
		"""
		return ResourceForm(self.client)

###############################################################################
# Class
###############################################################################

class Client:
	"""
	The client class is the backbone and manager of the SDK and mainly
	responsible for the communication and exchange of information 
	with Coscine servers.

	Attributes
	-----------
	language : str, "en" or "de"
		Language preset for input forms and form data.
	version : str
		Contains the current version string of the python SDK.
	logger : Logger
		An instance of the coscine.Logger class for cli/file output.
	session : requests.Session
		A requests session for the communication with Coscine servers.
	vocabularies : VocabularyManager
		Local cache server for nonvolatile data from Coscine.
	forms : FormManager (Use as FormManager.project/resource/metadata)
		Serves empty InputForms
	"""

	_language: str
	logger: Logger
	cache: Cache
	vocabularies: VocabularyManager
	forms: FormManager
	session: requests.Session
	concurrent: bool

	@property
	def version(self) -> str: return __version__

	@property
	def language(self) -> str: return self._language

	@language.setter
	def language(self, lang: str) -> None:
		lang = lang.lower()
		if lang in LANGUAGES:
			self._language = lang
		else:
			raise ValueError(f"Invalid value for argument 'lang' -> [{lang}]!\n"
									f"Possible values are {str(LANGUAGES)}.")

###############################################################################

	def __init__(self, token: str, lang: str = "en", logger: Logger = None,
			persistent_cache: bool = True, concurrent: bool = True) -> None:
		"""
		Initializes an instance of the base class of the Coscine Python SDK.

		Parameters
		----------
		token : str
			A Coscine API access token.
		lang : str, "en" or "de", default: "en"
			Language preset for input form fields and vocabularies.
		logger : Logger
			Sets a logger object for command line or file output.
		persistent_caching : bool, default: True
			Enable to store the cache in a file on deinitialization of
			the client object. Will attempt to load the cache file
			on initialization if enabled. Leads to a significant speed
			boost when making static requests right after init, but may
			also lead to invalid data when using outdated cache data, in case
			the Coscine API changed recently. However this is mostly avoided
			by performing frequent updates. Useful for applications with
			a short runtime that get run often.
		concurrent : bool, default: True
			If enabled, a ThreadPool is used for bulk requests, speeding up
			up- and downloads of multiple files tremendously.
		"""

		self.language = lang
		self.concurrent = concurrent
		enableLogging = False
		# If we are running from a command line
		if sys.stdout != None and sys.stderr.isatty():
			enableLogging = True
		self.logger = logger if logger else Logger(enableLogging, sys.stdout)
		self.cache = Cache(persistent_cache)
		self.vocabularies = VocabularyManager(self)
		self.forms = FormManager(self)
		self.session = requests.Session()
		self.session.headers = {
			"Authorization": f"Bearer {token}",
			"User-Agent": f"Coscine Python SDK {self.version}"
		}
		self.logger.banner()

###############################################################################

	@staticmethod
	def uri(api: str, endpoint: str, *args) -> str:
		"""
		Constructs a URL for performing a request to the Coscine API.

		Parameters
		----------
		api : str
			The target Coscine API endpoint, e.g. Blob, Metadata, Tree, ...
		endpoint : str
			The subendpoint of `api`.
		*args
			Variable number of arguments of type string to append to the URL.
			Arguments are automatically seperated by a slash '/' and
			special characters are encoded.
		
		Raises
		------
		ValueError
			If an invalid value is given as an argument to the method.

		Returns
		-------
		str
			Encoded URL for communication with the Coscine servers.
		"""

		BASE = "https://coscine.rwth-aachen.de/coscine/api/Coscine.Api.%s/%s"
		ENDPOINTS = (
			"Blob",
			"Metadata",
			"Organization",
			"Project",
			"Resources",
			"Tree",
			"User",
			"Search",
			"ActivatedFeatures"
		)

		if api not in ENDPOINTS:
			raise ValueError("Invalid value for argument 'api'!\n" \
						"Possible values are %s." % str(ENDPOINTS))
		
		uri = BASE % (api, endpoint)
		for arg in args:
			if arg is None:
				continue
			uri += "/" + urllib.parse.quote(arg, safe="")
		return uri

###############################################################################

	def _request(self, method: str, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a HTTP request to the Coscine Servers.

		Parameters
		----------
		method : str
			HTTP request method (GET, PUT, POST, DELETE).
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional keyword arguments forwarded to the requests library.
		
		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		# Normalize data before sending
		if "data" in kwargs and type(kwargs["data"]) is dict:
			kwargs["headers"] = {
				"Content-Type": "application/json;charset=utf-8"
			}
			kwargs["data"] = json.dumps(kwargs["data"])

		try:
			self.logger.net(f"{method} {uri}\n{json.dumps(kwargs, indent=4)}")
		except (JSONDecodeError, TypeError):
			pass

		# Perform the request and handle any resulting errors
		try:
			response = self.session.request(method, uri, **kwargs)
			response.raise_for_status()
			self.logger.net(f"response: {response.content}")
			return response
		except requests.exceptions.ConnectionError:
			raise ConnectionError
		except requests.exceptions.RequestException as e:
			if e.response.status_code == 401:
				raise AuthorizationError("Invalid Coscine API token!")
			else:
				raise ClientError()

###############################################################################

	def get(self, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a GET request to the Coscine API.

		Parameters
		----------
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional keyword arguments forwarded to the requests library.
		
		Examples
		--------
		>>> uri = client.uri("Project", "Project")
		>>> projects = client.get(uri).json()

		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		return self._request("GET", uri, **kwargs)

###############################################################################

	def put(self, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a PUT request to the Coscine API.

		Parameters
		----------
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional keyword arguments forwarded to the requests library.
		
		Examples
		--------
		>>> uri = self.uri("Tree", "Tree", resource.id, filename)
		>>> self.put(uri, data = metadata)

		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		return self._request("PUT", uri, **kwargs)

###############################################################################

	def post(self, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a POST request to the Coscine API.

		Parameters
		----------
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional arguments forwarded to the requests library.
		
		Examples
		--------
		>>> data = member.data
		>>> data["projectId"] = self.id
		>>> data["role"]["displayName"] = role
		>>> data["role"]["id"] = ProjectMember.ROLES[role]
		>>> uri = self.uri("Project", "ProjectRole")
		>>> self.post(uri, data = data)

		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		return self._request("POST", uri, **kwargs)

###############################################################################

	def delete(self, uri: str, **kwargs) -> requests.Response:
		"""
		Performs a DELETE request to the Coscine API.

		Parameters
		----------
		uri : str
			Coscine URL generated with Client.uri(...).
		**kwargs
			Additional keyword arguments forwarded to the requests library.
		
		Examples
		--------
		>>> uri = self.uri("Project", "Project", self.id)
		>>> self.delete(uri)

		Raises
		------
		coscine.exceptions.ConnectionError
			If the Coscine servers could not be reached.
		coscine.exceptions.AuthorizationError
			If the Coscine API token is invalid.
		coscine.exceptions.ClientError
			If the request resulted in an error.

		Returns
		-------
		requests.Response
			The response of the Coscine server as a requests.Response object.
		"""

		return self._request("DELETE", uri, **kwargs)

###############################################################################

	def static_request(self, uri: str) -> dict:
		"""
		Performs a GET request for the given uri. If such a request
		has been performed previously during the session, the previous
		response is returned. Otherwise a new request is made to Coscine
		and that response is then stored inside the session cache.

		Parameters
		-----------
		uri : str
			Request URI
		
		Returns
		-------
		dict
		"""

		data = self.cache.get(uri)
		if not data:
			data = self.get(uri).json()
			self.cache.set(uri, data)
		return data

###############################################################################

	def projects(self, toplevel: bool = True, **kwargs) -> List[Project]:
		"""
		Retrieves a list of a all projects the creator of the Coscine API token
		is currently a member of.

		Parameters
		----------
		toplevel : bool, default: True
			Retrieve only toplevel projects (no subprojects).
			Set to False if you want to retrieve all projects, regardless
			of hierarchy.
		**kwargs
			Project filter values.
			-> e.g. displayName="MyProject"
			-> Returns all projects with the specified displayName

		Returns
		-------
		list
			List of coscine.Project objects
		"""

		ENDPOINTS = ("Project", "Project/-/topLevel")
		uri = self.uri("Project", ENDPOINTS[toplevel])
		projects = []
		for it in self.get(uri).json():
			for key, value in kwargs.items():
				if it[key] != value:
					break
			else:
				projects.append(Project(self, it))
		return projects

###############################################################################

	def project(self, displayName: str = None, toplevel: bool = True,
												**kwargs) -> Project:
		"""
		Retrieves a single project the owner of the Coscine
		API token is currently a member of. Search criteria
		must be specified.

		Parameters
		----------
		displayName : str, default: None
			Default displayName search argument. May be omitted
			in favor of different arguments given in $kwargs. Allows
			easier use as `client.project("name")`.
		toplevel : bool, default: True
			Search only within toplevel projects (no subprojects)
			Set to False if you want to search through all projects,
			regardless of hierarchy.
		**kwargs (mandatory!)
			Project filter values.
			-> e.g. displayName="MyProject"
			-> Returns one project matching the specified displayName

		Raises
		-------
		OverflowError
			If more than one project match the specified search criteria.

		Returns
		-------
		Project
			coscine.Project object if a project matches the specifed filter.
		None
			if no project matching the filter was found.
		"""

		# Handle Arguments
		if displayName:
			kwargs["displayName"] = displayName
		elif not kwargs:
			raise ValueError("Not enough arguments!")

		# Filter projects
		projects = self.projects(toplevel, **kwargs)
		if len(projects) == 1:
			return projects[0]
		elif len(projects) == 0:
			return None
		else:
			raise OverflowError("More than 1 project matching criteria!")

###############################################################################

	def create_project(self, form: ProjectForm) -> Project:
		"""
		Creates a project using the given ProjectForm.

		Parameters
		----------
		form : ProjectForm
			ProjectForm filled with project metadata.

		Returns
		-------
		Project
			Project object of the new project.
		"""

		if type(form) is ProjectForm:
			form = form.generate()

		uri = self.uri("Project", "Project")
		return Project(self, self.post(uri, data=form).json())

###############################################################################

	def object(self, path: str) -> FileObject:
		"""
		Returns an object for a path

		Parameters
		----------
		path : str
			In format of "Project/Resource/filepath.filetype"

		Returns
		-------
		FileObject
		"""

		parts = path.split("/")
		if len(parts) < 3:
			raise ValueError("Not enough components in path. Must be > 2.")
		filepath = "/".join(parts[2:])
		return self.project(parts[0]).resource(parts[1]).object(filepath)

###############################################################################

	def search(self, query: str) -> dict:
		"""
		Performs a search query on Coscine
		"""

		uri = self.uri("Search", f"SemanticSearch?query={query}")
		results = self.get(uri).json()
		return results

###############################################################################