import os

from smart_emails.domain.run import Run
from smart_emails.drive_data.drive_attribute_file_reader import DriveAttributeFileReader
from smart_emails.drive_data.drive_attribute_file_writer import DriveAttributeFileWriter
from smart_emails.helpers.settings import Settings


class DriveAttributeProvider:
	def __init__(self,
				 drive_attribute_file_writer: DriveAttributeFileWriter,
				 drive_attribute_file_reader: DriveAttributeFileReader,
				 settings: Settings):
		self.file_writer = drive_attribute_file_writer
		self.file_reader = drive_attribute_file_reader
		self.settings = settings

	def get_current_previous_and_initial_runs(self) -> (Run, Run, Run):
		self.file_writer.retrieve_and_write_attributes_reading_to_file()

		attribute_files = os.listdir(self.settings.drive_directory_path)
		attribute_files.remove(self.settings.info_file_name)
		attribute_files.sort()

		current_attributes_reading = self.file_reader.get_attribute_readings_from_file(
			attribute_files[-1]) if len(attribute_files) > 0 else None

		initial_attribute_reading = self.file_reader.get_attribute_readings_from_file(
			attribute_files[0]) if len(attribute_files) > 1 else None

		previous_attribute_reading = self.file_reader.get_attribute_readings_from_file(
			attribute_files[-2]) if len(attribute_files) > 2 else None

		return current_attributes_reading, previous_attribute_reading, initial_attribute_reading
