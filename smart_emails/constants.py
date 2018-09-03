import os
from .helpers.singleton import Singleton


@Singleton
class Constants:

	def __init__(self):
		self.package_directory = ''
		self.attribute_file_name_format = 'SmartAttributes_%Y_%m_%d_%H_%M_%S'
		self.info_file_name = 'info.txt'
		self.config_file_name = "config.ini"
		self.email_template_relative_file_path = "foundation.emails/src/pages/smart-notification-template.html"


	@property
	def config_file_path(self) -> str:
		return os.path.join(self.package_directory, self.config_file_name)


	@property
	def history_directory(self) -> str:
		return os.path.join(self.package_directory, "history")


	def drive_directory(self, drive_serial_number) -> str:
		return os.path.join(self.history_directory, drive_serial_number)


	def drive_info_file_path(self, drive_serial_number) -> str:
		return os.path.join(self.drive_directory(drive_serial_number), self.info_file_name)


	@property
	def email_template_file_path(self) -> str:
		return os.path.join(self.package_directory, self.email_template_relative_file_path)


	def uninlined_email_file_path(self, drive_serial_number: str) -> str:
		return os.path.join(
			self.package_directory,
			"foundation.emails/src/pages/smart-notification_" + drive_serial_number + ".html")


	def inlined_email_file_path(self,drive_serial_number:str) -> str:
		return os.path.join(
			self.package_directory,
			"foundation.emails/dist/smart-notification_" + drive_serial_number + ".html")


	@property
	def inlining_tool_dir(self) -> str:
		return os.path.join(self.package_directory, "foundation.emails")
