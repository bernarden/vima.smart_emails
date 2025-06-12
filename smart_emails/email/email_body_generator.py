import os

from premailer import transform

from smart_emails.domain.drive_info import DriveInfo
from smart_emails.domain.run import Run
from smart_emails.helpers.settings import Settings


class EmailBodyGenerator:

	def __init__(self, settings: Settings):
		self.settings = settings
		self.info_columns = ["Model Family", "Device Model", "Serial Number", "User Capacity"]
		self.column_names_current = ["id", "name", "value", "worst", "thresh", "raw_value"]
		self.column_names = ["value", "worst", "thresh", "raw_value"]
		self.int_columns = ["value", "worst", "thresh"]

	def generate(self, run_list: tuple[Run, Run, Run], drive_info: DriveInfo) -> str:
		email_template = self.__get_email_template()
		header = self.__generate_header_html()
		rows = self.__generate_table_rows_html(run_list)
		info = self.__generate_info_html(drive_info)
		date = run_list[0].date
		email = self.__inject_email_content(email_template, self.settings.drive_identifier, date, info, header, rows)
		inlined_email = transform(email, remove_classes=True, capitalize_float_margin=True, allow_network=False)

		# Useful for debugging styling and inlining.
		# self.__store_email_to_file(email, inlined_email, drive_info.serial_number)
		return inlined_email

	def __get_email_template(self):
		with open(self.settings.email_template_file_path, "r") as f:
			template = f.read()
		return template

	@staticmethod
	def __inject_email_content(template, smartctl_drive_identifier, date, info, header, rows):
		template = template.replace("$DRIVE_PATH", smartctl_drive_identifier)
		template = template.replace("$RUN_TIME", date.strftime("%d/%m/%Y %H:%M"))
		template = template.replace("$INFO", info)
		template = template.replace("$ATTRIBUTES", header + rows)
		return template

	def __store_email_to_file(self, email: str, inlined_email: str, drive_serial_number: str) -> None:
		uninlined_file_path = os.path.join(
			self.settings.drive_directory_path,
			"smart_notification_" + drive_serial_number + ".html")
		with open(uninlined_file_path, "w+") as f:
			f.write(email)

		inlined_file_path = os.path.join(
			self.settings.drive_directory_path,
			"smart_notification_" + drive_serial_number + "_inlined.html")
		with open(inlined_file_path, "w+") as f:
			f.write(inlined_email)

	def __generate_info_html(self, drive_info: DriveInfo):
		info = ""
		for i in self.info_columns:
			if drive_info.values.get(i) is None:
				continue

			info += "<div class=\"info-section__info-row\">"
			info += "\n<div class=\"info-section__info-row--name\">" + i + "</div>"
			info += "\n<div class=\"info-section__info-row--value\">" + drive_info.values.get(i) + "</div>"
			info += "\n</div>"
		return info

	def __generate_header_html(self):
		header = "<tr class=\"attributes-table__headers-row\">"
		for i in self.column_names_current:
			header += "\n<th>" + i.upper() + "</th>"
		header += "\n</tr>"
		return header

	def __generate_table_rows_html(self, run_list):
		table_rows = ""
		number_rows = len(run_list[0].attributes)
		for i in range(0, number_rows):
			table_rows += self.__generate_current_row(run_list[0].attributes[i])
			if run_list[1] is not None:
				table_rows += (self.__generate_previous_row(run_list[1].attributes[i], run_list[1].date))
			if run_list[2] is not None:
				table_rows += (self.__generate_baseline_row(run_list[2].attributes[i], run_list[2].date))
		return table_rows

	def __generate_current_row(self, attribute):
		row = "<tr class=\"attributes-table__current-reading\">"
		for i in self.column_names_current:
			if i in self.int_columns:
				row += "\n<td style=\"text-align: center\">" + getattr(attribute, i) + "</td>"
			else:
				row += "\n<td>" + getattr(attribute, i) + "</td>"
		row += "\n</tr>"
		return row

	def __generate_previous_row(self, attribute, date):
		row = "<tr class=\"attributes-table__previous-reading\">"
		row += "\n<td></td>"
		row += "\n<td>Previous " + date.strftime("%d/%m/%Y") + "</td>"
		for i in self.column_names:
			if i in self.int_columns:
				row += "\n<td style=\"text-align: center\">" + getattr(attribute, i) + "</td>"
			else:
				row += "\n<td>" + getattr(attribute, i) + "</td>"
		row += "\n</tr>"
		return row

	def __generate_baseline_row(self, attribute, date):
		row = "<tr class=\"attributes-table__original-reading\">"
		row += "\n<td></td>"
		row += "\n<td>Original " + date.strftime("%d/%m/%Y") + "</td>"
		for i in self.column_names:
			if i in self.int_columns:
				row += "\n<td style=\"text-align: center\">" + getattr(attribute, i) + "</td>"
			else:
				row += "\n<td>" + getattr(attribute, i) + "</td>"
		row += "\n</tr>"
		return row
