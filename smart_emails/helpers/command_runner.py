import ctypes
import os
import subprocess
from shutil import which


class CommandRunner:

	@staticmethod
	def run_command(executable: str, arguments: str, requires_admin: bool = False) -> bytes:
		command = executable + " " + arguments
		if requires_admin and not (CommandRunner.is_admin()):
			raise Exception("Execution of command: '{}' requires administrator privileges.".format(command))

		if which(executable) is None:
			raise Exception("Can't execute requested command. Executable '{}' is not found.".format(executable))

		try:
			process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
			(output, err) = process.communicate()
			if err is None:
				return output
			else:
				raise Exception("Executed command '{}' returned an error: {}.".format(command, err))
		except Exception as e:
			raise Exception("Failed to execute command: '{}'".format(command)) from e

	@staticmethod
	def is_admin():
		try:
			is_admin = (os.getuid() == 0)
		except AttributeError:
			is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
		return is_admin
