import os

from smart_emails.domain.drive_info import DriveInfo
from smart_emails.helpers.command_runner import CommandRunner
from smart_emails.helpers.settings import Settings


class DriveInfoProvider:
	def __init__(self, settings: Settings):
		self.settings = settings

	def get_drive_info(self) -> DriveInfo:
		drive_info_output = CommandRunner.run_command(
			"smartctl", "-i " + self.settings.drive_identifier, True)

		dictionary = {}
		drive_info_output_lines = drive_info_output.decode("utf-8").split(os.linesep)
		for i, line in enumerate(drive_info_output_lines):
			# disregard header information in file
			if i > 3 and line.strip():
				key, value = line.split(':', 1)
				dictionary[key.strip()] = value.strip()
		drive_info = DriveInfo(dictionary)

		# Set drive's serial number in settings to generate directory paths.
		self.settings.set_drive_serial_number(drive_info.serial_number)

		# Create drive folder if it doesn't exist.
		os.makedirs(self.settings.drive_directory_path, exist_ok=True)

		# Write drive info into a file.
		with open(self.settings.drive_info_file_path, "w+b") as f:
			f.write(drive_info_output)

		return drive_info
