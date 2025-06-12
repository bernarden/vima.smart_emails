import os
from unittest.mock import patch

from smart_emails.drive_data.drive_info_provider import DriveInfoProvider
from tests.fixtures.drive_info_fixtures import SMARTCTL_SEAGATE_IRONWOLF_HDD, SMARTCTL_TOSHIBA_HDD, \
	SMARTCTL_SAMSUNG_NVME, \
	SMARTCTL_UNKNOWN_NVME
from tests.test_helpers.settings_test_helper import SettingsTestHelper


class TestDriveInfoProvider:
	def test_smartctl_output_written_to_file_correctly(self):
		# Arrange
		settings, stack = SettingsTestHelper.create_temp_settings()
		mock_command = stack.enter_context(patch(
			"smart_emails.helpers.command_runner.CommandRunner.run_command",
			return_value=SMARTCTL_SEAGATE_IRONWOLF_HDD))

		with stack:
			# Act
			DriveInfoProvider(settings).get_drive_info()

			# Assert
			mock_command.assert_called_once_with("smartctl", "-i /dev/sda", True)
			assert os.path.exists(settings.drive_info_file_path)
			with open(settings.drive_info_file_path, "rb") as f:
				content = f.read()
				assert content == SMARTCTL_SEAGATE_IRONWOLF_HDD

	def test_seagate_ironwolf_hdd_drive_info_mapped_correctly(self):
		# Arrange
		settings, stack = SettingsTestHelper.create_temp_settings()
		stack.enter_context(patch(
			"smart_emails.helpers.command_runner.CommandRunner.run_command",
			return_value=SMARTCTL_SEAGATE_IRONWOLF_HDD))

		with stack:
			# Act
			drive_info = DriveInfoProvider(settings).get_drive_info()

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
		settings, stack = SettingsTestHelper.create_temp_settings()
		stack.enter_context(patch(
			"smart_emails.helpers.command_runner.CommandRunner.run_command",
			return_value=SMARTCTL_TOSHIBA_HDD))

		with stack:
			# Act
			drive_info = DriveInfoProvider(settings).get_drive_info()

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
		settings, stack = SettingsTestHelper.create_temp_settings()
		stack.enter_context(patch(
			"smart_emails.helpers.command_runner.CommandRunner.run_command",
			return_value=SMARTCTL_SAMSUNG_NVME))

		with stack:
			# Act
			drive_info = DriveInfoProvider(settings).get_drive_info()

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

	def test_unknown_nvme_drive_info_mapped_correctly(self):
		# Arrange
		settings, stack = SettingsTestHelper.create_temp_settings()
		stack.enter_context(patch(
			"smart_emails.helpers.command_runner.CommandRunner.run_command",
			return_value=SMARTCTL_UNKNOWN_NVME))

		with stack:
			# Act
			drive_info = DriveInfoProvider(settings).get_drive_info()

			# Assert
			assert drive_info.model_family == "N/A"
			assert drive_info.device_model == "N/A"
			assert drive_info.model_number == "ABC012D3(EF)"
			assert drive_info.serial_number == "AB000000000000001234"
			assert drive_info.firmware_version == "AB01234"
			assert drive_info.user_capacity == "N/A"
			assert drive_info.total_nvm_capacity == "512,110,190,592 [512 GB]"
			assert drive_info.sector_size == "N/A"
			assert drive_info.sector_sizes == "N/A"
			assert drive_info.rotation_rate == "N/A"
			assert drive_info.device_is == "N/A"
			assert drive_info.ata_version_is == "N/A"
			assert drive_info.nvme_version == "1.4"
			assert drive_info.sata_version_is == "N/A"
			assert drive_info.local_time_is == "Fri May  9 18:00:00 2025 NZST"
			assert drive_info.smart_support_enabled == "N/A"
