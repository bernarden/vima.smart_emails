import sys

from smart_emails.drive_data.drive_attribute_file_reader import DriveAttributeFileReader
from smart_emails.drive_data.drive_attribute_file_writer import DriveAttributeFileWriter
from smart_emails.drive_data.drive_attribute_provider import DriveAttributeProvider
from smart_emails.drive_data.drive_info_provider import DriveInfoProvider
from smart_emails.email.email_body_generator import EmailBodyGenerator
from smart_emails.email.email_sender import EmailSender
from smart_emails.helpers.settings import Settings


def main() -> None:
	# Dependencies
	drive_identifier = sys.argv[1:][0]
	settings = Settings(drive_identifier)
	drive_info_provider = DriveInfoProvider(settings)
	drive_attribute_file_writer = DriveAttributeFileWriter(settings)
	drive_attribute_file_reader = DriveAttributeFileReader(settings)
	drive_attribute_provider = DriveAttributeProvider(
		drive_attribute_file_writer, drive_attribute_file_reader, settings)
	email_body_generator = EmailBodyGenerator(settings)
	email_sender = EmailSender(settings)

	# Execution
	settings.initialise()
	drive_info = drive_info_provider.get_drive_info()
	current_previous_and_initial_runs = drive_attribute_provider.get_current_previous_and_initial_runs()
	email_body = email_body_generator.generate(current_previous_and_initial_runs, drive_info)
	email_sender.send_html_email("SMART attributes for " + settings.drive_serial_number, email_body)


if __name__ == '__main__':
	main()
