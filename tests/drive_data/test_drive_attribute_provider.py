import os
from datetime import datetime
from unittest.mock import MagicMock

from smart_emails.domain.attribute import Attribute
from smart_emails.domain.run import Run
from smart_emails.drive_data.drive_attribute_file_reader import DriveAttributeFileReader
from smart_emails.drive_data.drive_attribute_file_writer import DriveAttributeFileWriter
from smart_emails.drive_data.drive_attribute_provider import DriveAttributeProvider
from smart_emails.helpers.settings import Settings
from tests.test_helpers.settings_test_helper import SettingsTestHelper


class TestDriveAttributeProvider:

	@staticmethod
	def create_info_and_attribute_files(settings: Settings, file_names):
		os.makedirs(settings.drive_directory_path, exist_ok=True)

		# Create dummy info.txt
		with open(settings.drive_info_file_path, "w") as f:
			f.write("Drive Info")

		# Create test files
		for name in file_names:
			path = os.path.join(settings.drive_directory_path, name)
			with open(path, "w") as f:
				f.write("Fake SMART data")

	@staticmethod
	def mock_reader_and_writer() -> tuple[MagicMock, MagicMock]:
		mock_writer = MagicMock(spec_arg=DriveAttributeFileWriter)
		mock_reader = MagicMock(spec_arg=DriveAttributeFileReader)
		mock_reader.get_attribute_readings_from_file.side_effect = \
			lambda file_name: Run(
				attributes=[Attribute(["", "", "", file_name, "", "", "", "", "", ""])],
				date=datetime.now()
			)

		return mock_writer, mock_reader

	def test_returns_none_when_no_files_exist(self):
		# Arrange
		file_names = []
		settings, stack = SettingsTestHelper.create_temp_settings()
		settings.set_drive_serial_number("ABC123")
		self.create_info_and_attribute_files(settings, file_names)
		mock_writer, mock_reader = self.mock_reader_and_writer()

		with stack:
			# Act
			current, previous, initial = DriveAttributeProvider(
				mock_writer,
				mock_reader,
				settings).get_current_previous_and_initial_runs()

			# Assert
			mock_writer.retrieve_and_write_attributes_reading_to_file.assert_called_once()
			mock_reader.get_attribute_readings_from_file.assert_not_called()
			assert current is None
			assert previous is None
			assert initial is None

	def test_returns_only_current_when_1_file_exists(self):
		file_names = ["2024-01-01-00-00-00.txt"]
		settings, stack = SettingsTestHelper.create_temp_settings()
		settings.set_drive_serial_number("ABC123")
		self.create_info_and_attribute_files(settings, file_names)
		mock_writer, mock_reader = self.mock_reader_and_writer()

		with stack:
			# Act
			current, previous, initial = DriveAttributeProvider(
				mock_writer,
				mock_reader,
				settings).get_current_previous_and_initial_runs()

			# Assert
			mock_writer.retrieve_and_write_attributes_reading_to_file.assert_called_once()
			assert mock_reader.get_attribute_readings_from_file.call_count == 1
			assert current is not None
			assert current.attributes[0].value == "2024-01-01-00-00-00.txt"
			assert previous is None
			assert initial is None

	def test_returns_current_and_initial_when_2_files_exist(self):
		file_names = ["2024-01-01-00-00-00.txt", "2024-01-02-00-00-00.txt"]
		settings, stack = SettingsTestHelper.create_temp_settings()
		settings.set_drive_serial_number("ABC123")
		self.create_info_and_attribute_files(settings, file_names)
		mock_writer, mock_reader = self.mock_reader_and_writer()

		with stack:
			# Act
			current, previous, initial = DriveAttributeProvider(
				mock_writer,
				mock_reader,
				settings).get_current_previous_and_initial_runs()

			# Assert
			mock_writer.retrieve_and_write_attributes_reading_to_file.assert_called_once()
			assert mock_reader.get_attribute_readings_from_file.call_count == 2
			assert current is not None
			assert current.attributes[0].value == "2024-01-02-00-00-00.txt"
			assert previous is None
			assert initial is not None
			assert initial.attributes[0].value == "2024-01-01-00-00-00.txt"

	def test_returns_all_when_3_files_exist(self):
		file_names = [
			"2024-01-01-00-00-00.txt",
			"2024-01-02-00-00-00.txt",
			"2024-01-03-00-00-00.txt"
		]
		settings, stack = SettingsTestHelper.create_temp_settings()
		settings.set_drive_serial_number("ABC123")
		self.create_info_and_attribute_files(settings, file_names)
		mock_writer, mock_reader = self.mock_reader_and_writer()

		with stack:
			# Act
			current, previous, initial = DriveAttributeProvider(
				mock_writer,
				mock_reader,
				settings).get_current_previous_and_initial_runs()

			# Assert
			mock_writer.retrieve_and_write_attributes_reading_to_file.assert_called_once()
			assert mock_reader.get_attribute_readings_from_file.call_count == 3
			assert current is not None
			assert current.attributes[0].value == "2024-01-03-00-00-00.txt"
			assert previous is not None
			assert previous.attributes[0].value == "2024-01-02-00-00-00.txt"
			assert initial is not None
			assert initial.attributes[0].value == "2024-01-01-00-00-00.txt"

	def test_returns_all_when_4_or_more_files_exist(self):
		file_names = [
			"2024-01-01-00-00-00.txt",
			"2024-01-02-00-00-00.txt",
			"2024-01-03-00-00-00.txt",
			"2024-01-04-00-00-00.txt",
		]
		settings, stack = SettingsTestHelper.create_temp_settings()
		settings.set_drive_serial_number("ABC123")
		self.create_info_and_attribute_files(settings, file_names)
		mock_writer, mock_reader = self.mock_reader_and_writer()

		with stack:
			# Act
			current, previous, initial = DriveAttributeProvider(
				mock_writer,
				mock_reader,
				settings).get_current_previous_and_initial_runs()

			# Assert
			mock_writer.retrieve_and_write_attributes_reading_to_file.assert_called_once()
			assert mock_reader.get_attribute_readings_from_file.call_count == 3
			assert current is not None
			assert current.attributes[0].value == "2024-01-04-00-00-00.txt"
			assert previous is not None
			assert previous.attributes[0].value == "2024-01-03-00-00-00.txt"
			assert initial is not None
			assert initial.attributes[0].value == "2024-01-01-00-00-00.txt"
