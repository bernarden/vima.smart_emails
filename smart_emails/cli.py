import os
import sys
import configparser
from smart_emails.constants import Constants
from smart_emails.drive_info_provider import DriveInfoProvider
from smart_emails.drive_attribute_provider import DriveAttributeProvider
from smart_emails.email_body_generator import EmailBodyGenerator
from smart_emails.email_sender import EmailSender


def main() -> None:
	arguments: [] = sys.argv[1:]
	process_runtime_variables()
	create_config_file_if_doesnt_exist()
	create_history_folder()
	smartctl_drive_identifier = get_drive_identifier(arguments)
	drive_info = DriveInfoProvider().get_drive_info(smartctl_drive_identifier)
	current_previous_and_initial_runs = DriveAttributeProvider(drive_info.serial_number).get_current_previous_and_initial_runs(smartctl_drive_identifier)
	email_body = EmailBodyGenerator().generate(current_previous_and_initial_runs, drive_info, smartctl_drive_identifier)
	EmailSender.send_html_email("SmartCheck results for " + smartctl_drive_identifier, email_body)


def get_drive_identifier(arguments: []) -> str:
	return arguments[0]


def create_history_folder() -> None:
	if not os.path.exists(Constants.instance().history_directory):
		os.mkdir(Constants.instance().history_directory)


def process_runtime_variables() -> None:
	Constants.instance().package_directory = os.path.dirname(os.path.abspath(__file__))


def create_config_file_if_doesnt_exist() -> None:
	config = configparser.ConfigParser()
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

	if not os.path.exists(Constants.instance().config_file_path):
		with open(Constants.instance().config_file_path, 'w+') as configfile:
			config.write(configfile)


if __name__ == '__main__':
	main()
