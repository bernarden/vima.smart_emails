import os
import tempfile
from contextlib import ExitStack
from unittest.mock import patch

from smart_emails.helpers.settings import Settings  # Assuming your Settings class is in this path


class SettingsTestHelper:
	@staticmethod
	def create_temp_settings(drive_identifier: str = "/dev/sda") -> tuple[Settings, ExitStack]:
		stack = ExitStack()

		tmp_dir = stack.enter_context(tempfile.TemporaryDirectory())
		mock_config_file_path = os.path.join(tmp_dir, "test_config.ini")
		patch_env = patch.dict(os.environ, {"SMART_EMAILS__CONFIG_FILE_PATH": mock_config_file_path})
		stack.enter_context(patch_env)

		settings = Settings(drive_identifier)
		settings.history_directory_path = os.path.join(tmp_dir, settings.history_directory_path)

		return settings, stack
