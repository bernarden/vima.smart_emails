#!/usr/bin/env python3

import datetime
import subprocess
import os

class EmailBodyGenerator:
	package_directory = os.path.dirname(os.path.abspath(__file__))

	def generate(self, run_list, drive_info, drive_name):
		template = self.read_template()

		# TODO: Rename
		# Current log displays the most information
		global column_names_current
		column_names_current = ["id","name","value","worst","thresh","raw_value"]

		# Used for previous and baseline rows
		global column_names
		column_names = ["value","worst","thresh","raw_value"]

		# integer values rendered differently in css
		global int_columns
		int_columns = ["value","worst","thresh"]

		header = self.generate_header()

		rows = self.generate_table_rows(run_list)

		template = self.inject_content(template, drive_name, run_list[0].date, drive_info, header, rows)

		self.write_file(template, drive_name)
		self.inline_css()

	def read_template(self):
		with open(os.path.join(self.package_directory, "foundation.emails/src/pages/smart-notification-template.html"), "r") as f:
			template = f.read()
		return template

	def generate_header(self):
		header = "<tr class=\"attributes-table__headers-row\">"
		for i in column_names_current:
			header += "\n<th>" + i.upper() + "</th>"
		header += "\n</tr>"
		return header

	def generate_table_rows(self, run_list):
		table_rows = ""

		number_rows = len(run_list[0].attributes)

		for i in range(0, number_rows):
			table_rows += self.generate_current_row(run_list[0].attributes[i])
			if(run_list[1] is not None):
				table_rows += (self.generate_previous_row(run_list[1].attributes[i], run_list[1].date))
			if(run_list[2] is not None):
				table_rows += (self.generate_baseline_row(run_list[2].attributes[i], run_list[2].date))
		return table_rows

	def generate_current_row(self, attribute):
		row = "<tr class=\"attributes-table__current-reading\">"
		for i in column_names_current:
			if (i in int_columns):
				row += "\n<td style=\"text-align: center\">" + getattr(attribute, i) + "</td>"
			else:
				row += "\n<td>" + getattr(attribute, i) + "</td>"
		row += "\n</tr>"
		return row

	def generate_previous_row(self, attribute, date):
		row = "<tr class=\"attributes-table__previous-reading\">"
		row += "\n<td></td>"
		row += "\n<td>Previous " + date.strftime("%d/%m/%Y") + "</td>"
		for i in column_names:
			if (i in int_columns):
				row += "\n<td style=\"text-align: center\">" + getattr(attribute, i) + "</td>"
			else:
				row += "\n<td>" + getattr(attribute, i) + "</td>"
		row += "\n</tr>"
		return row

	def generate_baseline_row(self, attribute, date):
		row = "<tr class=\"attributes-table__original-reading\">"
		row += "\n<td></td>"
		row += "\n<td>Original " + date.strftime("%d/%m/%Y") + "</td>"
		for i in column_names:
			if (i in int_columns):
				row += "\n<td style=\"text-align: center\">" + getattr(attribute, i) + "</td>"
			else:
				row += "\n<td>" + getattr(attribute, i) + "</td>"
		row += "\n</tr>"
		return row

	def inject_content(self, template, drive_name, date, info, header, rows):
		info_columns = ["$DRIVE_PATH", "$RUN_TIME", "$MODEL_FAMILY", "$DEVICE_MODEL", "$SERIAL_NUMBER", "$CAPACITY"]

		template = template.replace("$DRIVE_PATH", drive_name)
		template = template.replace("$RUN_TIME", date.strftime("%d/%m/%Y"))
		template = template.replace("$MODEL_FAMILY", info.model_family)
		template = template.replace("$DEVICE_MODEL", info.device_model)
		template = template.replace("$SERIAL_NUMBER", info.serial_number)
		template = template.replace("$CAPACITY", info.user_capacity)

		template = template.replace("$ATTRIBUTES", header+rows)

		return template

	def inject_info(self, template, info):
		info_columns = ["$DRIVE_PATH", "$RUN_TIME", "$MODEL_FAMILY", "$DEVICE_MODEL", "$SERIAL_NUMBER", "$CAPACITY"]

		#template[index].replace("$DRIVE_PATH", )

		index = template.index("$ATTRIBUTES")
		template[index] = header
		for i in rows:
			template.insert(index + 1, i)
			index += 1
		return template

	def inject_rows(self, template, header, rows):
		index = self.index_containing_substring(template, "$ATTRIBUTES")
		template[index] = header
		for i in rows:
			template.insert(index + 1, i)
			index += 1
		return template

	def write_file(self, template, drive_name):
		now = datetime.datetime.now()
		file = os.path.join(self.package_directory, "foundation.emails/src/pages/smart-notification_" + drive_name + "_" + now.strftime("%d_%m_%Y") +".html")
		with open(file, "w+") as f:
			f.write(template)

	def inline_css(self):
		command = "npm install"

		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, cwd = os.path.join(self.package_directory,"foundation.emails"))
		output, error = process.communicate()

		command = "npm run-script build"

		process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, cwd = os.path.join(self.package_directory,"foundation.emails"))
		output, error = process.communicate()