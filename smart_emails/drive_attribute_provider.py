import os

from smart_emails.constants import Constants
from smart_emails.domain.run import Run
from smart_emails.helpers.drive_attribute_file_reader import DriveAttributeFileReader
from smart_emails.helpers.drive_attribute_file_writer import DriveAttributeFileWriter


class DriveAttributeProvider:

	@staticmethod
	def get_current_previous_and_initial_runs(
			smartctl_drive_identifier: str, drive_serial_number: str) -> (Run, Run, Run):
		DriveAttributeFileWriter.retrieve_and_write_attributes_reading_to_file(
			smartctl_drive_identifier, drive_serial_number)

		attribute_files = os.listdir(Constants.instance().drive_directory(drive_serial_number))
		attribute_files.remove("info.txt")
		attribute_files.sort()

		current_attributes_reading = DriveAttributeFileReader.get_attribute_readings_from_file(
			drive_serial_number, attribute_files[-1]) if len(attribute_files) > 0 else None

		initial_attribute_reading = DriveAttributeFileReader.get_attribute_readings_from_file(
			drive_serial_number, attribute_files[0]) if len(attribute_files) > 1 else None

		previous_attribute_reading = DriveAttributeFileReader.get_attribute_readings_from_file(
			drive_serial_number, attribute_files[-2]) if len(attribute_files) > 2 else None

		return current_attributes_reading, previous_attribute_reading, initial_attribute_reading
