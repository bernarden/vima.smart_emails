from smart_emails.domain.run import Run
from smart_emails.drive_data.drive_attribute_file_reader import DriveAttributeFileReader
from tests.fixtures.drive_attributes_fixtures import SMARTCTL_HHD1_ATTRIBUTES_SCAN1
from tests.test_helpers.attribute_file_helper import AttributeFileHelper
from tests.test_helpers.settings_test_helper import SettingsTestHelper


class TestDriveAttributeFileReader:
	def test_reads_and_parses_attribute_file(self):
		# Arrange
		settings, stack = SettingsTestHelper.create_temp_settings()
		settings.set_drive_serial_number("ABC123")
		timestamp, filename = AttributeFileHelper.generate_file(settings, SMARTCTL_HHD1_ATTRIBUTES_SCAN1)

		with stack:
			# Act
			result = DriveAttributeFileReader(settings).get_attribute_readings_from_file(filename)

			# Assert
			assert isinstance(result, Run)
			assert result.date == timestamp
			assert len(result.attributes) == 18

			expected_attrs = [
				["1", "Raw_Read_Error_Rate", "0x000b", "100", "100", "001", "Pre-fail", "Always", "-", "0"],
				["2", "Throughput_Performance", "0x0004", "136", "136", "054", "Old_age", "Offline", "-", "96"],
				["3", "Spin_Up_Time", "0x0007", "083", "083", "001", "Pre-fail", "Always", "-", "339 (Average 341)"],
				["4", "Start_Stop_Count", "0x0012", "100", "100", "000", "Old_age", "Always", "-", "25"],
				["5", "Reallocated_Sector_Ct", "0x0033", "100", "100", "001", "Pre-fail", "Always", "-", "0"],
				["7", "Seek_Error_Rate", "0x000a", "100", "100", "001", "Old_age", "Always", "-", "0"],
				["8", "Seek_Time_Performance", "0x0004", "140", "140", "020", "Old_age", "Offline", "-", "15"],
				["9", "Power_On_Hours", "0x0012", "098", "098", "000", "Old_age", "Always", "-", "16947"],
				["10", "Spin_Retry_Count", "0x0012", "100", "100", "001", "Old_age", "Always", "-", "0"],
				["12", "Power_Cycle_Count", "0x0032", "100", "100", "000", "Old_age", "Always", "-", "25"],
				["22", "Unknown_Attribute", "0x0023", "100", "100", "025", "Pre-fail", "Always", "-", "100"],
				["192", "Power-Off_Retract_Count", "0x0032", "100", "100", "000", "Old_age", "Always", "-", "750"],
				["193", "Load_Cycle_Count", "0x0012", "100", "100", "000", "Old_age", "Always", "-", "750"],
				["194", "Temperature_Celsius", "0x0002", "060", "060", "000", "Old_age", "Always", "-",
				 "34 (Min/Max 20/47)"],
				["196", "Reallocated_Event_Count", "0x0032", "100", "100", "000", "Old_age", "Always", "-", "0"],
				["197", "Current_Pending_Sector", "0x0022", "100", "100", "000", "Old_age", "Always", "-", "0"],
				["198", "Offline_Uncorrectable", "0x0008", "100", "100", "000", "Old_age", "Offline", "-", "0"],
				["199", "UDMA_CRC_Error_Count", "0x000a", "100", "100", "000", "Old_age", "Always", "-", "0"],
			]
			for i, expected in enumerate(expected_attrs):
				attr = result.attributes[i]
				assert [attr.id, attr.name, attr.flag, attr.value, attr.worst, attr.thresh,
						attr.att_type, attr.updated, attr.when_failed, attr.raw_value] == expected
