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
This file defines the project object for the representation of
Coscine projects. It provides a simple interface to interact with Coscine
projects from python.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
	from .client import Client
from .exceptions import *
from .resource import Resource, ResourceForm
from .form import InputForm
from .defaults import TIMEFORMAT
from prettytable.prettytable import PrettyTable
from datetime import datetime
from urllib.parse import urljoin, urlparse
import json
import os

###############################################################################
# Class definition
###############################################################################

class ProjectForm(InputForm):
	"""
	"""

	parent: Project

###############################################################################

	def __init__(self, client: Client, parent: Project = None) -> None:
		self._items = client.vocabularies.builtin("project")
		self.parent = parent
		super().__init__(client)
		vocabularies = {
			"disciplines": client.vocabularies.disciplines(True),
			"organizations": client.vocabularies.organizations(True),
			"visibility": client.vocabularies.visibility(True)
		}
		for item in self._items:
			if item.vocabulary:
				self._vocabularies[item.path] = vocabularies[item.path]

###############################################################################

	def _parse_organizations(self, data):
		organizations = []
		for value in data:
			organization = {
				#"displayName": urljoin(value["displayName"], urlparse(value["displayName"]).path),
				"url": urljoin(value["url"], urlparse(value["url"]).path)
			}
			organizations.append(organization)
			# organization vocabualry only contains 1st 100 entries
			# can only filter, not get full
		return organizations

###############################################################################

	def parse(self, data: dict) -> None:
		IGNORE = ["id", "slug", "parentId"]
		if data is None:
			return
		for path, value in data.items():
			if path in IGNORE: continue
			if path == "organizations":
				value = self._parse_organizations(value)
			key = self.name_of(path)
			self.set_value(key, value, True)

###############################################################################

	def generate(self) -> dict:
		"""
		"""

		metadata = {}
		missing = []

		for key, values in self.items(True):
			if not values:
				if self.is_required(key):
					missing.append(key)
				continue

			properties = self.properties(key)
			path = properties.path
			metadata[path] = values if properties.maxCount > 1 else values[0]

		if missing:
			raise ValueError(missing)

		if self.parent:
			metadata["ParentId"] = self.parent.id
		
		return metadata

###############################################################################
# Class definition
###############################################################################

class Project:
	"""
	Python representation of a Coscine Project
	"""

	client: Client
	data: dict
	parent: Project

	id: str
	name: str
	displayName: str
	description: str
	principleInvestigators: str
	startDate: datetime
	endDate: datetime
	disciplines: List[str]
	organizations: List[str]
	visibility: str

	###############################################################################

	def __init__(self, client: Client, data: dict,
					parent: Project = None) -> None:
		"""
		Initializes a Coscine project object.

		Parameters
		----------
		client : Client
			Coscine client handle
		data : dict
			Project data received from Coscine.
		parent : Project
			Optional parent project.
		"""

		self.client = client
		self.data = data
		self.parent = parent

###############################################################################

	@property
	def id(self) -> str: return self.data["id"]

	@property
	def name(self) -> str: return self.data["projectName"]

	@property
	def displayName(self) -> str: return self.data["displayName"]

	@property
	def description(self) -> str: return self.data["description"]

	@property
	def principleInvestigators(self) -> str:
		return self.data["principleInvestigators"]

	@property
	def startDate(self) -> datetime:
		return datetime.strptime(self.data["startDate"], TIMEFORMAT)

	@property
	def endDate(self) -> datetime:
		return datetime.strptime(self.data["endDate"], TIMEFORMAT)

	@property
	def disciplines(self) -> List[str]:
		lang = {
			"en": "displayNameEn",
			"de": "displayNameDe"
		}[self.client.language]
		return [k[lang] for k in self.data["disciplines"]]
	
	@property
	def organizations(self) -> List[str]:
		return[k["displayName"] for k in self.data["organizations"]]
	
	@property
	def visibility(self) -> str: return self.data["visibility"]["displayName"]

###############################################################################

	def __str__(self) -> str:
		table = PrettyTable(("Property", "Value"))
		rows = [
			("ID", self.id),
			("Name", self.name),
			("Display Name", self.displayName),
			("Principle Investigators", self.principleInvestigators),
			("Disciplines", "\n".join(self.disciplines)),
			("Organizations", "\n".join(self.organizations)),
			("Start Date", self.startDate),
			("End Date", self.endDate),
			("Visibility", self.visibility)
		]
		table.max_width["Value"] = 50
		table.add_rows(rows)
		return table.get_string(title = "Project [%s]" % self.displayName)

###############################################################################

	def subprojects(self, **kwargs) -> List[Project]:
		"""
		Retrieves a list of subprojects of the current project matching a set
		of specified filters

		Parameters
		----------
		kwargs
			key-value filters for subprojects (e.g. 'Name' = 'My Project').

		Returns
		-------
		list of Projects
		"""

		uri = self.client.uri("Project", "SubProject", self.id)
		projects = self.client.get(uri).json()
		filter = []
		for data in projects:
			match = True
			for key, value in kwargs.items():
				if data[key] != value:
					match = False
					break
			if match:
				filter.append(Project(self.client, data, self))
		return filter

###############################################################################

	def delete(self) -> None:
		"""
		Deletes the project on the Coscine servers.
		"""

		uri = self.client.uri("Project", "Project", self.id)
		self.client.delete(uri)

###############################################################################

	def resources(self, **kwargs) -> List[Resource]:
		"""
		Retrieves a list of Resources of the current project matching a set
		of specified filters.

		Parameters
		----------
		kwargs
			key-value filters for resources (e.g. 'Name' = 'My Resource').
		
		Returns
		-------
		list[Resource]
			list of resources matching the supplied filter.
		"""

		uri = self.client.uri("Project", "Project", self.id, "resources")
		resources = []
		for it in self.client.get(uri).json():
			for key, value in kwargs.items():
				if it[key] != value:
					break
			else:
				resources.append(Resource(self, it))
		return resources

###############################################################################

	def resource(self, displayName: str = None, **kwargs) -> Resource:
		"""
		Retrieves a certain resource of the current project matching a set
		of specified filters or identified by its displayName.

		Parameters
		----------
		displayName : str
			The display name of the resource.
		kwargs
			key-value filters for resources (e.g. 'Name' = 'My Resource').
		
		Returns
		--------
		Resource or None
		"""
		
		if displayName:
			kwargs["displayName"] = displayName
		elif not kwargs:
			raise ValueError("")

		resources = self.resources(**kwargs)
		if len(resources) == 1:
			return resources[0]
		elif len(resources) == 0:
			return None
		else:
			raise ValueError("Found more than 1 resource matching "\
										"the specified criteria!")

###############################################################################

	def download(self, path: str = "./", metadata: bool = False) -> None:
		"""
		Downloads the project to the location referenced by 'path'.

		Parameters
		----------
		path : str
			Download location on the harddrive
			Default: current directory './'
		metadata : bool, default: False
			If enabled, project metadata is downloaded and put in
			a hidden file '.metadata.json'.
		"""

		path = os.path.join(path, self.displayName)
		if not os.path.isdir(path):
			os.mkdir(path)
		for resource in self.resources():
			resource.download(path=path, metadata=metadata)
		if metadata:
			data = json.dumps(self.data, indent=4)
			fd = open(os.path.join(path, ".metadata.json"), "w")
			fd.write(data)
			fd.close()

###############################################################################

	def members(self) -> List[ProjectMember]:
		"""
		Retrieves a list of all members of the current project

		Returns
		--------
		list[ProjectMember]
			List of project members as ProjectMember objects.
		"""

		uri = self.client.uri("Project", "ProjectRole", self.id)
		data = self.client.get(uri).json()
		members = [ProjectMember(self, m) for m in data]
		return members

###############################################################################

	def invite(self, email: str, role: str = "Member") -> None:
		"""
		Invites a person to a project via their email address

		Parameters
		----------
		email : str
			The email address to send the invite to
		role : str, "Member" or "Owner", default: "Member"
			The role for the new project member
		"""

		if role not in ProjectMember.ROLES:
			raise ValueError("Invalid role '%s'." % role)

		uri = self.client.uri("Project", "Project", "invitation")
		data = {
			"projectId": self.data["id"],
			"role": ProjectMember.ROLES[role],
			"email": email
		}

		try:
			self.client.log("Inviting [%s] as [%s] to project [%s]." % 
												(email, role, self.id))
			self.client.post(uri, data = data)
		except ServerError:
			self.client.log("User [%s] has invite pending." % email)

###############################################################################

	def add_member(self, member: ProjectMember, role: str = "Member"):
		"""
		Adds a project member of another project to the current project.

		Parameters
		----------
		member : ProjectMember
			Member of another Coscine project
		role : str, "Member" or "Owner", default: "Member"
		"""

		if role not in ProjectMember.ROLES:
			raise ValueError("Invalid role!")

		data = member.data
		data["projectId"] = self.id
		data["role"]["displayName"] = role
		data["role"]["id"] = ProjectMember.ROLES[role]
		uri = self.client.uri("Project", "ProjectRole")
		self.client.post(uri, data = data)

###############################################################################

	def form(self) -> ProjectForm:
		"""
		"""

		form = ProjectForm(self.client)
		form.parse(self.data)
		return form

###############################################################################

	def update(self, form: ProjectForm) -> dict:
		"""
		Updates a project using the given ProjectForm

		Parameters
		----------
		form : ProjectForm
			ProjectForm containing updated data.
		"""

		if type(form) is ProjectForm:
			form = form.generate()
		uri = self.client.uri("Project", "Project", self.id)
		response = self.client.post(uri, data = form)
		if response.ok: self.data = response.json()
		return response

###############################################################################

	def create_resource(self, form: ResourceForm) -> Resource:
		"""
		Creates a resource within the current project using the supplied
		resource form.

		Parameters
		----------
		resourceForm : ResourceForm
			Form to generate the resource with.
		metadataPreset : MetadataPresetForm
			optional application profile configuration.
		"""
		if type(form) is ResourceForm:
			form = form.generate()
		uri = self.client.uri("Resources", "Resource", "Project", self.id)
		return Resource(self, self.client.post(uri, data = form).json())

###############################################################################
# Class definition
###############################################################################

class ProjectMember:

	"""
	Initializes a project member for a given project.

	Parameters
	----------
	project : Project
		Coscine python SDK project handle.
	data: dict
		User data as dict, retrieved via 
		client.uri("Project", "ProjectRole", self.id).
	"""

	ROLES = {
		"Owner": "be294c5e-4e42-49b3-bec4-4b15f49df9a5",
		"Member": "508b6d4e-c6ac-4aa5-8a8d-caa31dd39527"
	}

	name: str
	email: str
	id: str
	role: str
	data: dict
	client: Client
	project: Project

###############################################################################

	def __init__(self, project: Project, data: dict) -> None:
		"""
		"""

		self.project = project
		self.client = self.project.client
		self.data = data
		self.name = data["user"]["displayName"]
		self.email = data["user"]["emailAddress"]
		self.id = data["user"]["id"]
		self.role = data["role"]["displayName"]

###############################################################################

	def set_role(self, role: str) -> None:

		"""
		Sets the role of a project member

		Parameters
		----------
		role : str
			The new role of the member ('Owner' or 'Member').
		"""

		ROLES = {
			"Owner": "be294c5e-4e42-49b3-bec4-4b15f49df9a5",
			"Member": "508b6d4e-c6ac-4aa5-8a8d-caa31dd39527"
		}

		if role not in ROLES:
			raise ValueError("Invalid role '%s'." % role)

		uri = self.client.uri("Project", "ProjectRole")
		self.data["role"]["id"] = ROLES[role]
		self.data["role"]["displayName"] = role
		self.client.post(uri, data = self.data)

###############################################################################

	def remove(self) -> None:
		"""
		Removes a project member from their associated project.
		"""

		uri = self.client.uri("Project", "ProjectRole", "project", \
			self.project.id, "user", self.id, "role", self.data["role"]["id"])
		self.client.delete(uri)

###############################################################################