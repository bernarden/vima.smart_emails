import os
import subprocess
from smart_emails.constants import Constants
from smart_emails.domain.drive_info import DriveInfo

class DriveInfoProvider:

	def get_drive_info(self, smartctl_drive_identifier: str) -> DriveInfo:
		drive_info_output = self.__run_command("smartctl -i " + smartctl_drive_identifier)

		dictionary = {}
		drive_info_output_lines = drive_info_output.decode("utf-8").split('\n')
		for i, line in enumerate(drive_info_output_lines):
			# disregard header information in file
			if i > 3 and line.strip():
				dictionary[line[:18].strip()] = line[18:].strip()
		drive_info = DriveInfo(dictionary)

		# Create drive folder if doesn't exist.
		drive_directory = Constants.instance().drive_directory(drive_info.serial_number)
		if not os.path.exists(drive_directory):
			os.mkdir(drive_directory)

		# Write drive info into a file.
		drive_info_file_path = Constants.instance().drive_info_file_path(drive_info.serial_number)
		with open(drive_info_file_path, "w+") as f:
			for line in drive_info_output_lines:
				f.writelines(line + '\n')

		return drive_info

	@staticmethod
	def __run_command(command: str) -> bytes:
		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
		(output, err) = process.communicate()
		# TODO - VU: Handle errors.
		return output
