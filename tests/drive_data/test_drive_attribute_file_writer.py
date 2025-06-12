import os
from datetime import datetime
from unittest.mock import patch

from smart_emails.drive_data.drive_attribute_file_writer import DriveAttributeFileWriter
from tests.fixtures.drive_attributes_fixtures import SMARTCTL_HHD2_ATTRIBUTES_SCAN1
from tests.test_helpers.settings_test_helper import SettingsTestHelper


class TestDriveAttributeFileWriter:
	def test_writes_smart_output_to_expected_file(self):
		# Arrange
		settings, stack = SettingsTestHelper.create_temp_settings()
		settings.set_drive_serial_number("ABC123")
		mock_command = stack.enter_context(
			patch("smart_emails.helpers.command_runner.CommandRunner.run_command",
				  return_value=SMARTCTL_HHD2_ATTRIBUTES_SCAN1)
		)
		fixed_time = datetime(2025, 1, 1, 12, 0, 0)
		mock_datetime = stack.enter_context(
			patch("smart_emails.drive_data.drive_attribute_file_writer.datetime", wraps=datetime)
		)
		mock_datetime.now.return_value = fixed_time

		with stack:
			# Act
			DriveAttributeFileWriter(settings).retrieve_and_write_attributes_reading_to_file()

			# Assert
			mock_command.assert_called_once_with("smartctl", "--attributes /dev/sda", True)
			expected_path = os.path.join(
				settings.drive_directory_path,
				fixed_time.strftime(settings.attribute_file_name_format))
			assert os.path.exists(expected_path)
			with open(expected_path, "rb") as f:
				content = f.read()
				assert content == SMARTCTL_HHD2_ATTRIBUTES_SCAN1
