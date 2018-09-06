import subprocess
import os
from smart_emails.constants import Constants


class EmailBodyGenerator:

	def __init__(self):
		self.column_names_current = ["id", "name", "value", "worst", "thresh", "raw_value"]
		self.column_names = ["value", "worst", "thresh", "raw_value"]
		self.int_columns = ["value", "worst", "thresh"]


	def generate(self, run_list, drive_info, smartctl_drive_identifier) -> str:
		email_template = self.__get_email_template()

		header = self.__generate_header()
		rows = self.__generate_table_rows(run_list)
		email = self.__inject_email_content(
			email_template, smartctl_drive_identifier, run_list[0].date, drive_info, header, rows)

		self.__store_email_to_file(email, drive_info.serial_number)
		self.__inline_css()
		return self.__get_inlined_email(drive_info.serial_number)


	@staticmethod
	def __get_email_template():
		template_file_path = Constants.instance().email_template_file_path
		with open(template_file_path, "r") as f:
			template = f.read()
		return template


	@staticmethod
	def __inject_email_content(template, smartctl_drive_identifier, date, info, header, rows):
		template = template.replace("$DRIVE_PATH", smartctl_drive_identifier)
		template = template.replace("$RUN_TIME", date.strftime("%d/%m/%Y %H:%M"))

		if info.model_family != "N/A":
			template = template.replace("$MODEL_FAMILY", info.model_family)
		else:
			template = template.replace("$MODEL_FAMILY", "")

		if info.device_model != "N/A":
			template = template.replace("$DEVICE_MODEL", info.device_model)
		else:
			template = template.replace("$DEVICE_MODEL", "")

		if info.serial_number != "N/A":
			template = template.replace("$SERIAL_NUMBER", info.serial_number)
		else:
			template = template.replace("$SERIAL_NUMBER", "")

		if info.user_capacity != "N/A":
			template = template.replace("$CAPACITY", info.user_capacity)
		else:
			template = template.replace("$CAPACITY", "")

		template = template.replace("$ATTRIBUTES", header + rows)

		return template

	@staticmethod
	def __store_email_to_file(email, drive_serial_number):
		file = os.path.join(Constants.instance().uninlined_email_file_path(drive_serial_number))
		with open(file, "w+") as f:
			f.write(email)


	def __generate_header(self):
		header = "<tr class=\"attributes-table__headers-row\">"
		for i in self.column_names_current:
			header += "\n<th>" + i.upper() + "</th>"
		header += "\n</tr>"
		return header


	def __generate_table_rows(self, run_list):
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


	@staticmethod
	def __inline_css():
		if not os.path.exists(os.path.join(Constants.instance().inlining_tool_dir, 'node_modules')):
			command = "npm install"
			process = subprocess.Popen(
				command.split(),
				stdout=subprocess.PIPE,
				cwd=Constants.instance().inlining_tool_dir, shell=True)
			process.communicate()

		command = "npm run-script build"
		process = subprocess.Popen(
			command.split(),
			stdout=subprocess.PIPE,
			cwd=Constants.instance().inlining_tool_dir, shell=True)
		process.communicate()

	@staticmethod
	def __get_inlined_email(drive_serial_number) -> str:
		with open(Constants.instance().inlined_email_file_path(drive_serial_number), "r") as f:
			return f.read()
