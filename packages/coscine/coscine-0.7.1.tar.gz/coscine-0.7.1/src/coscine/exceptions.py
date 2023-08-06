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
This file defines all of the exceptions raised by the Coscine Python SDK.
The base exception class is called CoscineException. It directly inherits
its properties from the standard Python Exception class.
Although never used directly it provides the basis for more specific
exceptions, thus allowing you to catch any Coscine exception with just one
except statement:
try:
	something()
except coscine.CoscineException: # Gotta Catch 'Em All
	print("Oh Dios Mio!")
"""

###############################################################################
# Class definition
###############################################################################

class CoscineException(Exception):
	"""
	Coscine base Exception class.
	"""

###############################################################################

class ConnectionError(CoscineException):
	"""
	A ConnectionError is raised in case the client is not able to establish
	a connection with the Coscine servers.
	"""
	pass

###############################################################################

class AuthorizationError(CoscineException):
	"""
	AuthorizationErrors are thrown in case of an invalid
	or empty Coscine ApiToken.
	"""
	pass

###############################################################################

class PermissionError(CoscineException):
	"""
	A PermissionError is thrown in cases where the owner of
	the Coscine API token does not hold enough privileges to access
	a certain path or perform a certain action.
	"""
	pass

###############################################################################

class ClientError(CoscineException):
	"""
	An ambiguous error has been made or detected on the client side.
	"""
	pass

###############################################################################

class ServerError(CoscineException):
	"""
	An ambiguous error has been made or detected on the Coscine server.
	"""
	pass

###############################################################################