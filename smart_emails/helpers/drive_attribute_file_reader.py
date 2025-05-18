import os
from datetime import datetime

from smart_emails.constants import Constants
from smart_emails.domain.attribute import Attribute
from smart_emails.domain.run import Run


class DriveAttributeFileReader:

	@staticmethod
	def get_attribute_readings_from_file(drive_serial_number: str, file_name: str) -> Run:
		attribute_file_path = os.path.join(Constants.instance().drive_directory(drive_serial_number), file_name)
		run_time = datetime.strptime(file_name, Constants.instance().attribute_file_name_format)
		attributes = []
		with open(attribute_file_path, "r") as f:
			for i, line in enumerate(f):
				# disregard header information in file
				if i > 6 and line.strip():
					attributes.append(Attribute(DriveAttributeFileReader.__extract_attribute_values(line)))
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
