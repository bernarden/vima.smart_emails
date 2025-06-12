import os
from configparser import ConfigParser


class Settings:
	def __init__(self, drive_identifier):
		self.config = ConfigParser()
		self.config_file_path = os.getenv("SMART_EMAILS__CONFIG_FILE_PATH", "config.ini")

		self.history_directory_path = "history"
		self.info_file_name = "info.txt"
		self.attribute_file_name_format = "smart_attributes_%Y_%m_%d_%H_%M_%S.txt"
		self.email_template_file_path = os.path.join("email", "html", "smart_notification_template.html")

		self.drive_identifier = drive_identifier
		self.drive_serial_number: str = ""
		self.drive_directory_path: str = ""
		self.drive_info_file_path: str = ""

		self.mail_server: str = ""
		self.mail_port: int = 0
		self.mail_use_tls: bool = False
		self.mail_use_ssl: bool = True
		self.mail_username: str = ""
		self.mail_password: str = ""
		self.mail_from: str = ""
		self.mail_to: str = ""

	def initialise(self):
		if not os.path.exists(self.config_file_path):
			self.__create_default_config_file()
		self.config.read(self.config_file_path)

		section = "DEFAULTS"
		self.history_directory_path = self.__get_str_value(
			section, "history_directory_path", self.history_directory_path)
		self.info_file_name = self.__get_str_value(
			section, "info_file_name", self.info_file_name)
		self.attribute_file_name_format = self.__get_str_value(
			section, "attribute_file_name_format", self.attribute_file_name_format)
		self.email_template_file_path = self.__get_str_value(
			section, "email_template_file_path", self.email_template_file_path)

		section = "MAIL"
		self.mail_server = self.__get_str_value(section, "server", self.mail_server)
		self.mail_port = self.get_int_value(section, "port", self.mail_port)
		self.mail_use_tls = self.__get_boolean_value(section, "use_tls", self.mail_use_tls)
		self.mail_use_ssl = self.__get_boolean_value(section, "use_ssl", True)
		self.mail_username = self.__get_str_value(section, "username", self.mail_username)
		self.mail_password = self.__get_str_value(section, "password", self.mail_password)
		self.mail_from = self.__get_str_value(section, "from", self.mail_from)
		self.mail_to = self.__get_str_value(section, "to", self.mail_to)

	def set_drive_serial_number(self, drive_serial_number: str):
		self.drive_serial_number = drive_serial_number
		self.drive_directory_path = os.path.join(self.history_directory_path, drive_serial_number)
		self.drive_info_file_path = os.path.join(self.drive_directory_path, self.info_file_name)

	def __get_str_value(self, section: str, name: str, default: str) -> str:
		return self.__get_value(section, name, default)

	def __get_boolean_value(self, section: str, name: str, default: bool) -> bool:
		str_value = self.__get_value(section, name, default)
		if str_value is None: return default
		return str_value.lower() in ("yes", "true", "t", "1")

	def get_int_value(self, section: str, name: str, default: int) -> int:
		str_value = self.__get_value(section, name, default)
		if str_value is None: return default
		try:
			return int(str_value)
		except ValueError:
			print(
				f"Warning: Could not convert config value '{str_value}' for [{section}]{name} to integer. Using default: {default}")
			return default

	def __get_value(self, section: str, name: str, default: any) -> str:
		file_value = (
			self.config.get(section, name, fallback=default)
			if self.config.has_section(section) or self.config.defaults()
			else default
		)
		env_var_name = f"SMART_EMAILS__{name.upper()}"
		return os.getenv(env_var_name, file_value)

	def __create_default_config_file(self) -> None:
		with open(self.config_file_path, 'w') as configFile:
			config = ConfigParser()
			config['DEFAULTS'] = {
				'history_directory_path': self.history_directory_path,
				'info_file_name': self.info_file_name,
				'attribute_file_name_format': self.attribute_file_name_format.replace('%', '%%'),
				'email_template_file_path': self.email_template_file_path
			}
			config['MAIL'] = {
				'SERVER': 'smtp.gmail.com',
				'PORT': 465,
				'USE_TLS': False,
				'USE_SSL': True,
				'USERNAME': 'username@gmail.com',
				'PASSWORD': 'password',
				'FROM': 'username@gmail.com',
				'TO': 'username@gmail.com'
			}
			config.write(configFile)
