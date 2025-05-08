import os
import tempfile
from contextlib import ExitStack
from unittest.mock import patch

from smart_emails.constants import Constants
from smart_emails.drive_info_provider import DriveInfoProvider
from tests.fixtures import SMARTCTL_SEAGATE_IRONWOLF_HDD, SMARTCTL_TOSHIBA_HDD, SMARTCTL_SAMSUNG_NVME


class TestDriveInfoProvider:
	@staticmethod
	def arrange_test(smartctl_output):
		tmpdir = tempfile.TemporaryDirectory()
		stack = ExitStack()
		stack.enter_context(tmpdir)
		mock_constants = stack.enter_context(patch.object(Constants, 'instance'))
		mock_constants.return_value.drive_directory = lambda s: tmpdir.name
		expected_file_path = os.path.join(tmpdir.name, "drive_info_file.txt")
		mock_constants.return_value.drive_info_file_path = lambda s: expected_file_path
		stack.enter_context(patch(
			"smart_emails.helpers.commandRunner.CommandRunner.run_command",
			return_value=smartctl_output))

		return expected_file_path

	def test_smartctl_output_written_to_file_correctly(self):
		# Arrange
		expected_file_path = self.arrange_test(SMARTCTL_SEAGATE_IRONWOLF_HDD)

		# Act
		DriveInfoProvider().get_drive_info("/dev/sda")

		# Assert
		assert os.path.exists(expected_file_path)
		with open(expected_file_path, "r") as f:
			content = f.read()
			expected_content = SMARTCTL_SEAGATE_IRONWOLF_HDD.decode() + "\n"
			assert content == expected_content

	def test_seagate_ironwolf_hdd_drive_info_mapped_correctly(self):
		# Arrange
		self.arrange_test(SMARTCTL_SEAGATE_IRONWOLF_HDD)

		# Act
		drive_info = DriveInfoProvider().get_drive_info("/dev/sda")

		# Assert
		assert drive_info.model_family == "Seagate IronWolf"
		assert drive_info.device_model == "ST1000VN123-0A1234"
		assert drive_info.model_number == "N/A"
		assert drive_info.serial_number == "ABC01D2E"
		assert drive_info.firmware_version == "AB01"
		assert drive_info.user_capacity == "1,000,195,402,752 bytes [1.00 TB]"
		assert drive_info.total_nvm_capacity == "N/A"
		assert drive_info.sector_size == "N/A"
		assert drive_info.sector_sizes == "512 bytes logical, 4096 bytes physical"
		assert drive_info.rotation_rate == "7200 rpm"
		assert drive_info.device_is == "In smartctl database 7.3/0123"
		assert drive_info.ata_version_is == "ACS-4 (minor revision not indicated)"
		assert drive_info.nvme_version == "N/A"
		assert drive_info.sata_version_is == "SATA 3.3, 6.0 Gb/s (current: 6.0 Gb/s)"
		assert drive_info.local_time_is == "Sat Jan 01 00:00:00 2000 NZDT"
		assert drive_info.smart_support_enabled == "Enabled"

	def test_toshiba_hdd_drive_info_mapped_correctly(self):
		# Arrange
		self.arrange_test(SMARTCTL_TOSHIBA_HDD)

		# Act
		drive_info = DriveInfoProvider().get_drive_info("/dev/sda")

		# Assert
		assert drive_info.model_family == "N/A"
		assert drive_info.device_model == "TOSHIBA AB0123CDEF"
		assert drive_info.model_number == "N/A"
		assert drive_info.serial_number == "A0BCD1E2F"
		assert drive_info.firmware_version == "AB012C"
		assert drive_info.user_capacity == "1,000,204,886,016 bytes [1.00 TB]"
		assert drive_info.total_nvm_capacity == "N/A"
		assert drive_info.sector_size == "N/A"
		assert drive_info.sector_sizes == "512 bytes logical, 4096 bytes physical"
		assert drive_info.rotation_rate == "5400 rpm"
		assert drive_info.device_is == "Not in smartctl database [for details use: -P showall]"
		assert drive_info.ata_version_is == "ATA8-ACS (minor revision not indicated)"
		assert drive_info.nvme_version == "N/A"
		assert drive_info.sata_version_is == "SATA 2.6, 3.0 Gb/s (current: 3.0 Gb/s)"
		assert drive_info.local_time_is == "Mon Jun 01 00:00:00 2020 NZST"
		assert drive_info.smart_support_enabled == "Enabled"

	def test_samsung_nvme_drive_info_mapped_correctly(self):
		# Arrange
		self.arrange_test(SMARTCTL_SAMSUNG_NVME)

		# Act
		drive_info = DriveInfoProvider().get_drive_info("/dev/sda")

		# Assert
		assert drive_info.model_family == "N/A"
		assert drive_info.device_model == "N/A"
		assert drive_info.model_number == "Samsung SSD 990 PRO 2TB"
		assert drive_info.serial_number == "A0B1CD2E345678F"
		assert drive_info.firmware_version == "0A1BCDE2"
		assert drive_info.user_capacity == "N/A"
		assert drive_info.total_nvm_capacity == "2,000,398,934,016 [2.00 TB]"
		assert drive_info.sector_size == "N/A"
		assert drive_info.sector_sizes == "N/A"
		assert drive_info.rotation_rate == "N/A"
		assert drive_info.device_is == "N/A"
		assert drive_info.ata_version_is == "N/A"
		assert drive_info.nvme_version == "2.0"
		assert drive_info.sata_version_is == "N/A"
		assert drive_info.local_time_is == "Thu May 08 00:00:00 2025 NZST"
		assert drive_info.smart_support_enabled == "N/A"
