import os
from datetime import datetime

from smart_emails.helpers.settings import Settings


class AttributeFileHelper:
	@staticmethod
	def generate_file(settings: Settings, smartctl_attribute_output: bytes) -> tuple[datetime, str]:
		os.makedirs(settings.drive_directory_path, exist_ok=True)

		timestamp = datetime.now().replace(microsecond=0)
		filename = timestamp.strftime(settings.attribute_file_name_format)
		attribute_file_path = os.path.join(settings.drive_directory_path, filename)

		with open(attribute_file_path, "wb") as f:
			f.write(smartctl_attribute_output)

		return timestamp, filename
