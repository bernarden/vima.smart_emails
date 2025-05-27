import os
from datetime import datetime

from smart_emails.constants import Constants
from smart_emails.helpers.command_runner import CommandRunner


class DriveAttributeFileWriter:

	@staticmethod
	def retrieve_and_write_attributes_reading_to_file(smartctl_drive_identifier: str, drive_serial_number: str) -> None:
		timestamp = datetime.now()
		output = CommandRunner.run_command("smartctl", "--attributes " + smartctl_drive_identifier, True)

		filename = timestamp.strftime(Constants.instance().attribute_file_name_format)
		file_path = os.path.join(Constants.instance().drive_directory(drive_serial_number), filename)
		with open(file_path, "w+b") as f:
			f.write(output)
