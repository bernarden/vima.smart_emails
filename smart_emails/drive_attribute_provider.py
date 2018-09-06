import os
import subprocess
from datetime import datetime
from smart_emails.domain.run import Run
from smart_emails.constants import Constants
from smart_emails.domain.attribute import Attribute


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
			initial_attribute_reading = self.__get_attribute_readings_from_file(attribute_files[0])
			return current_attributes_reading, None, initial_attribute_reading
		else:
			initial_attribute_reading = self.__get_attribute_readings_from_file(attribute_files[0])
			previous_attribute_reading = self.__get_attribute_readings_from_file(attribute_files[-2])
			return current_attributes_reading, previous_attribute_reading, initial_attribute_reading


	def __get_current_attributes_reading(self, smartctl_drive_identifier: str) -> Run:
		timestamp = datetime.now()
		output = self.__run_command("smartctl --attributes " + smartctl_drive_identifier)

		filename = timestamp.strftime(Constants.instance().attribute_file_name_format)
		file_path = os.path.join(Constants.instance().drive_directory(self.drive_serial_number), filename)
		with open(file_path, "w+b") as f:
			f.write(output)

		return self.__get_attribute_readings_from_file(filename)


	def __get_attribute_readings_from_file(self, file_name: str) -> Run:
		attribute_file_path = os.path.join(Constants.instance().drive_directory(self.drive_serial_number), file_name)
		run_time = datetime.strptime(file_name, Constants.instance().attribute_file_name_format)
		attributes = []
		with open(attribute_file_path, "r") as f:
			for i, line in enumerate(f):
				# disregard header information in file
				if i > 6 and line.strip():
					attributes.append(Attribute(self.__extract_attribute_values(line)))
		return Run(attributes, run_time)


	# String split method that handles whitespace in last column (Min/Max X)
	@staticmethod
	def __extract_attribute_values(line: str):
		values = line.split()
		# there should only be 10 columns
		# assume no issues with whitespace on the first 9 columns
		while len(values) > 10:
			values[9] += " " + values[10]
			values.pop(10)
		return values


	@staticmethod
	def __run_command(command: str) -> bytes:
		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
		(output, err) = process.communicate()
		# TODO - VU: Handle errors.
		return output
