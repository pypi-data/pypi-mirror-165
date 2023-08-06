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
This file provides a simple logger internally used by the Coscine Python SDK.
The logger is capable of printing information to a specified file handle
including warnings and debug information.
A ProgressBar and color handling is also provided.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from typing import TextIO, List, Callable
from enum import Enum
import sys
import platform
import colorama
from tqdm.auto import tqdm
from .__about__ import __version__

###############################################################################
# Class definition
###############################################################################

class LogLevel(Enum):
	DEBUG = 0
	WARN = 1
	NET = 2

###############################################################################
# Class definition
###############################################################################

class Colors:
	"""
	A simple class to handle colors in the terminal.
	"""

	BLUE: str = ""
	YELLOW: str = ""
	WHITE: str = ""

	@staticmethod
	def enable(enable: bool) -> None:
		"""
		Enable colors in command line output.
		"""

		if enable:
			Colors.BLUE = colorama.Fore.BLUE
			Colors.WHITE = colorama.Fore.WHITE
			Colors.YELLOW = colorama.Fore.YELLOW
		else:
			Colors.BLUE = Colors.WHITE = Colors.YELLOW = ""

###############################################################################
# Class definition
###############################################################################

class Logger:
	"""
	A simple logger class to handle standard output of the Coscine Python SDK.

	Attributes
	----------
	_stdout : TextIO
		The output file descriptor
	enabled : bool
		Enables/Disables command line output
	_loglevels : list
		A list of LogLevels to control the type of output of the logger.
	"""

	_stdout: TextIO
	enabled: bool
	_loglevels: List[LogLevel]

###############################################################################

	def __init__(self, enabled: bool, stdout: TextIO = sys.stdout,
						loglevels: List[LogLevel] = [LogLevel.WARN],
										colors: bool = True) -> None:
		"""
		Initializes an instance of the logger class.

		Parameters
		-----------
		enabled : bool
			Controls whether command line output is enabled.
		stdout : TextIO
			Overwrites the standard output file descriptor. Set to a file
			for logging to file.
		loglevels : List[LogLevel]
			Controls the type of output the logger makes.
		colors : bool
			Enables/Disables colored output. Should be
			disabled for logging to file.
		"""

		self._stdout = stdout
		self.enabled = enabled
		self.set_loglevels(loglevels)
		if colors:
			# Colorama overwrites sys.stdout, so special care is needed
			if self._stdout == sys.stdout:
				colorama.init()
				self._stdout = sys.stdout
				Colors.enable(True)

###############################################################################

	def banner(self) -> None:
		"""
		Prints an ASCII art banner of Coscine including
		the current SDK version to stdout.
		"""

		BANNER : str = f"""{Colors.BLUE} \
                    _             
                    (_)            
   ___ ___  ___  ___ _ _ __   ___  
  / __/ _ \/ __|/ __| | '_ \ / _ \ 
 | (_| (_) \__ \ (__| | | | |  __/ 
  \___\___/|___/\___|_|_| |_|\___| {Colors.WHITE}
____________________________________

    Coscine Python SDK {Colors.YELLOW}{__version__}{Colors.WHITE}
____________________________________
"""
		self.log(BANNER)

###############################################################################

	def set_loglevels(self, loglevels: List[LogLevel]) -> None:
		"""
		Set the loglevels of the logger to control what gets printed
		to the specified stdout file handle.

		Parameters
		----------
		loglevels : List[LogLevel]
			A list of LogLevel values
		
		Raises
		------
		ValueError
			In case the specified loglevels list contains an invalid loglevel.
		"""

		# Verify we got a valid loglevel
		for level in loglevels:
			if level not in LogLevel:
				raise ValueError(f"Specified LogLevel {level} is not \
												a valid loglevel!")

		# Apply loglevels
		self._loglevels = loglevels

###############################################################################

	def log(self, msg: str) -> None:
		"""
		If logging is enabled a message is printed to the specified
		stdout file handle.

		Parameters
		----------
		msg : str
			The message as a string.
		"""

		if self.enabled:
			print(msg, file=self._stdout)

###############################################################################

	def net(self, msg: str) -> None:
		"""
		Network traffic is printed to the specified stdout file handle if
		the loglevels include the LogLevel.NET level and logging is enabled.

		Parameters
		----------
		msg : str
			The message as a string.
		"""

		if LogLevel.NET in self._loglevels or LogLevel.DEBUG in self._loglevels:
			self.log("[NET] " + msg)

###############################################################################

	def warn(self, msg: str) -> None:
		"""
		A warning is printed to the specified stdout file handle if
		the loglevels include the LogLevel.WARN level and logging is enabled.

		Parameters
		----------
		msg : str
			The warning message as a string.
		"""

		if LogLevel.WARN in self._loglevels or LogLevel.DEBUG in self._loglevels:
			self.log("[WARNING] " + msg)

###############################################################################

	def debug(self, msg: str) -> None:
		"""
		A debug message is printed to the specified stdout file handle if
		the loglevels include the LogLevel.DEBUG level and logging is enabled.

		Parameters
		----------
		msg : str
			The debug message as a string.
		"""

		self.log("[DBG] " + msg)

###############################################################################

	@staticmethod
	def sysinfo() -> str:
		"""
		Constructs system information for better bug reports.

		Returns
		-------
		str
			Multiline string containing system and python information.
		"""

		info = \
		"""\
		Platform: %s
		Machine: %s
		Processor: %s
		Python compiler: %s
		Python branch: %s
		Python implementation: %s
		Python revision: %s
		Python version: %s
		""" % ( platform.platform(),
				platform.machine(),
				platform.processor(),
				platform.python_compiler(),
				platform.python_branch(),
				platform.python_implementation(),
				platform.python_revision(),
				platform.python_version()
			)
		return info.replace("\t", " ")

###############################################################################
# Class definition
###############################################################################

class ProgressBar:
	"""
	The ProgressBar class is a simple wrapper around tqdm
	progress bars. It is used in download/upload methods and provides the
	benefit of remembering state information and printing only when in
	verbose mode.

	Attributes
	----------
	logger : Logger
		Coscine Python SDK logger handle.
	bar : tqdm.tqdm
		tqdm Progress Bar instance.
	filesize : int
		Filesize in bytes.
	n : int
		Number of bytes read.
	callback : Callable[int]
		Callback function to call on update.
	"""

	logger: Logger
	bar: tqdm
	filesize: int
	n: int
	callback: Callable[[int]]

###############################################################################

	def __init__(self, logger: Logger, filesize: int, key: str, \
				mode: str, callback: Callable[[int]] = None) -> None:
		"""
		Initializes a state-aware tqdm ProgressBar.

		client : Client
			Coscine python SDK client handle
		filesize : int
			Size of the file object in bytes
		key : str
			key/filename of the file object
		mode : str
			'UP' or 'DOWN' referring to upload and download
		callafter : function(chunksize: int)
			 callback function to call after each update
		"""

		MODES = ("UP", "DOWN")

		if mode not in MODES:
			raise ValueError("Invalid value for argument 'mode'! " \
							"Possible values are %s." % str(MODES))

		self.logger = logger
		self.callback = callback
		self.filesize = filesize
		self.n = 0
		if self.logger.enabled:
			self.bar = tqdm(total=filesize, unit="B", unit_scale=True,
												desc="%s %s" % (mode, key))

###############################################################################

	def update(self, chunksize: int) -> None:
		"""
		Updates the progress bar with respect to the consumed chunksize.
		If a callafter function has been provided to the Constructor, it is
		called during the update.
		"""

		self.n += chunksize
		if self.logger.enabled:
			self.bar.update(chunksize)
			self.bar.refresh()
		if self.callback:
			self.callback(chunksize)

###############################################################################