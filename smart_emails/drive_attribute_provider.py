import os
from datetime import datetime

from smart_emails.constants import Constants
from smart_emails.domain.run import Run
from smart_emails.helpers.command_runner import CommandRunner
from smart_emails.helpers.drive_attribute_file_reader import DriveAttributeFileReader


class DriveAttributeProvider:

	def __init__(self, drive_serial_number: str):
		self.drive_serial_number = drive_serial_number

	def get_current_previous_and_initial_runs(self, smartctl_drive_identifier: str) -> (Run, Run, Run):
		current_attributes_reading = self.__get_current_attributes_reading(smartctl_drive_identifier)

		attribute_files = os.listdir(Constants.instance().drive_directory(self.drive_serial_number))
		attribute_files.remove("info.txt")
		attribute_files.sort()

		if len(attribute_files) == 1:
			return current_attributes_reading, None, None
		elif len(attribute_files) == 2:
			initial_attribute_reading = DriveAttributeFileReader.get_attribute_readings_from_file(
				self.drive_serial_number, attribute_files[0])
			return current_attributes_reading, None, initial_attribute_reading
		else:
			initial_attribute_reading = DriveAttributeFileReader.get_attribute_readings_from_file(
				self.drive_serial_number, attribute_files[0])
			previous_attribute_reading = DriveAttributeFileReader.get_attribute_readings_from_file(
				self.drive_serial_number, attribute_files[-2])
			return current_attributes_reading, previous_attribute_reading, initial_attribute_reading

	def __get_current_attributes_reading(self, smartctl_drive_identifier: str) -> Run:
		timestamp = datetime.now()
		output = CommandRunner.run_command("smartctl", "--attributes " + smartctl_drive_identifier, True)

		filename = timestamp.strftime(Constants.instance().attribute_file_name_format)
		file_path = os.path.join(Constants.instance().drive_directory(self.drive_serial_number), filename)
		with open(file_path, "w+b") as f:
			f.write(output)

		return DriveAttributeFileReader.get_attribute_readings_from_file(self.drive_serial_number, filename)
