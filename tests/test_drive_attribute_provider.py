import os
import tempfile
from contextlib import ExitStack
from datetime import datetime
from unittest.mock import patch

from smart_emails.constants import Constants
from smart_emails.domain.attribute import Attribute
from smart_emails.domain.run import Run
from smart_emails.drive_attribute_provider import DriveAttributeProvider


class TestDriveAttributeProvider:
	@staticmethod
	def arrange_test(file_names):
		tmpdir = tempfile.TemporaryDirectory()
		stack = ExitStack()
		stack.enter_context(tmpdir)

		mock_constants = stack.enter_context(patch.object(Constants, "instance"))
		mock_constants.return_value.drive_directory = lambda s: tmpdir.name
		mock_writer = stack.enter_context(patch(
			"smart_emails.helpers.drive_attribute_file_writer.DriveAttributeFileWriter.retrieve_and_write_attributes_reading_to_file"))
		mock_reader = stack.enter_context(patch(
			"smart_emails.helpers.drive_attribute_file_reader.DriveAttributeFileReader.get_attribute_readings_from_file",
			side_effect=lambda drive_serial_number, file_name: Run(
				[Attribute(["", "", "", file_name, "", "", "", "", "", ""])],
				datetime.now()
			)
		))

		# Create dummy info.txt
		with open(os.path.join(tmpdir.name, "info.txt"), "w") as f:
			f.write("Drive Info")

		# Create test files
		for name in file_names:
			path = os.path.join(tmpdir.name, name)
			with open(path, "w") as f:
				f.write("Fake SMART data")

		return tmpdir.name, stack, mock_writer, mock_reader

	def test_returns_none_when_no_files_exist(self):
		# Arrange
		file_names = []
		_, _, mock_writer, mock_reader = self.arrange_test(file_names)

		# Act
		current, previous, initial = DriveAttributeProvider.get_current_previous_and_initial_runs(
			"/dev/sda", "ABC123")

		# Assert
		mock_writer.assert_called_once()
		mock_reader.assert_not_called()
		assert current is None
		assert previous is None
		assert initial is None

	def test_returns_only_current_when_1_file_exists(self):
		filenames = ["2024-01-01-00-00-00.txt"]
		_, _, mock_writer, mock_reader = self.arrange_test(filenames)

		# Act
		current, previous, initial = DriveAttributeProvider.get_current_previous_and_initial_runs(
			"/dev/sda", "ABC123")

		# Assert
		mock_writer.assert_called_once()
		assert mock_reader.call_count == 1
		assert current is not None
		assert current.attributes[0].value == "2024-01-01-00-00-00.txt"
		assert previous is None
		assert initial is None

	def test_returns_current_and_initial_when_2_files_exist(self):
		filenames = ["2024-01-01-00-00-00.txt", "2024-01-02-00-00-00.txt"]
		_, _, mock_writer, mock_reader = self.arrange_test(filenames)

		# Act
		current, previous, initial = DriveAttributeProvider.get_current_previous_and_initial_runs(
			"/dev/sda", "ABC123")

		# Assert
		mock_writer.assert_called_once()
		assert mock_reader.call_count == 2
		assert current is not None
		assert current.attributes[0].value == "2024-01-02-00-00-00.txt"
		assert previous is None
		assert initial is not None
		assert initial.attributes[0].value == "2024-01-01-00-00-00.txt"

	def test_returns_all_when_3_files_exist(self):
		filenames = [
			"2024-01-01-00-00-00.txt",
			"2024-01-02-00-00-00.txt",
			"2024-01-03-00-00-00.txt"
		]
		_, _, mock_writer, mock_reader = self.arrange_test(filenames)

		# Act
		current, previous, initial = DriveAttributeProvider.get_current_previous_and_initial_runs(
			"/dev/sda", "ABC123")

		# Assert
		mock_writer.assert_called_once()
		assert mock_reader.call_count == 3
		assert current is not None
		assert current.attributes[0].value == "2024-01-03-00-00-00.txt"
		assert previous is not None
		assert previous.attributes[0].value == "2024-01-02-00-00-00.txt"
		assert initial is not None
		assert initial.attributes[0].value == "2024-01-01-00-00-00.txt"

	def test_returns_all_when_4_or_more_files_exist(self):
		filenames = [
			"2024-01-01-00-00-00.txt",
			"2024-01-02-00-00-00.txt",
			"2024-01-03-00-00-00.txt",
			"2024-01-04-00-00-00.txt",
		]
		_, _, mock_writer, mock_reader = self.arrange_test(filenames)

		# Act
		current, previous, initial = DriveAttributeProvider.get_current_previous_and_initial_runs(
			"/dev/sda", "ABC123")

		# Assert
		mock_writer.assert_called_once()
		assert mock_reader.call_count == 3
		assert current is not None
		assert current.attributes[0].value == "2024-01-04-00-00-00.txt"
		assert previous is not None
		assert previous.attributes[0].value == "2024-01-03-00-00-00.txt"
		assert initial is not None
		assert initial.attributes[0].value == "2024-01-01-00-00-00.txt"
