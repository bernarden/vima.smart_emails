import os
from datetime import datetime

from smart_emails.helpers.command_runner import CommandRunner
from smart_emails.helpers.settings import Settings


class DriveAttributeFileWriter:
	def __init__(self, settings: Settings):
		self.settings = settings

	def retrieve_and_write_attributes_reading_to_file(self) -> None:
		timestamp = datetime.now()
		output = CommandRunner.run_command(
			"smartctl", "--attributes " + self.settings.drive_identifier, True)

		os.makedirs(self.settings.drive_directory_path, exist_ok=True)

		filename = timestamp.strftime(self.settings.attribute_file_name_format)
		file_path = os.path.join(self.settings.drive_directory_path, filename)
		with open(file_path, "w+b") as f:
			f.write(output)
