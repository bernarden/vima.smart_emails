import os
import tempfile
from contextlib import ExitStack
from datetime import datetime
from unittest.mock import patch

from smart_emails.constants import Constants
from smart_emails.helpers.drive_attribute_file_writer import DriveAttributeFileWriter
from tests.fixtures.drive_attributes_fixtures import SMARTCTL_HHD2_ATTRIBUTES_SCAN1


class TestDriveAttributeFileWriter:

	@staticmethod
	def arrange_test():
		tmpdir = tempfile.TemporaryDirectory()
		stack = ExitStack()
		stack.enter_context(tmpdir)

		# Patch Constants
		mock_constants = stack.enter_context(patch.object(Constants, "instance"))
		mock_constants.return_value.drive_directory = lambda s: tmpdir.name
		mock_constants.return_value.attribute_file_name_format = "%Y-%m-%d-%H-%M-%S.txt"

		# Patch CommandRunner
		mock_command = stack.enter_context(
			patch("smart_emails.helpers.command_runner.CommandRunner.run_command",
				  return_value=SMARTCTL_HHD2_ATTRIBUTES_SCAN1)
		)

		# Patch datetime
		fixed_time = datetime(2024, 1, 1, 12, 0, 0)
		mock_datetime = stack.enter_context(patch("smart_emails.helpers.drive_attribute_file_writer.datetime"))
		mock_datetime.now.return_value = fixed_time
		mock_datetime.strptime = datetime.strptime
		mock_datetime.strftime = datetime.strftime

		return tmpdir.name, fixed_time, stack, mock_command

	def test_writes_smart_output_to_expected_file(self):
		# Arrange
		directory, fixed_time, stack, mock_command = self.arrange_test()

		# Act
		DriveAttributeFileWriter.retrieve_and_write_attributes_reading_to_file("/dev/sda", "ABC123")

		# Assert
		mock_command.assert_called_once_with("smartctl", "--attributes /dev/sda", True)
		expected_path = os.path.join(directory, fixed_time.strftime("%Y-%m-%d-%H-%M-%S.txt"))
		assert os.path.exists(expected_path)
		with open(expected_path, "rb") as f:
			content = f.read()
			assert content == SMARTCTL_HHD2_ATTRIBUTES_SCAN1
