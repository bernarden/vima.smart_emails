#!/usr/bin/env python3

"""A script to send notifications about SMART attributes."""

import subprocess
import os
import datetime
import smtplib
import configparser
from smart_emails.domain.attribute import Attribute
from smart_emails.domain.run import Run
from smart_emails.domain.info import Info
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smart_emails.email_body_generator import EmailBodyGenerator
from re import compile

drive_path = ''
drive_directory = ''
package_directory = os.path.dirname(os.path.abspath(__file__))


def main(arguments):
	# First argument should be hard drive location
	initialize(arguments[0])

	# Create info.txt file if required
	write_drive_info()
	# Create Smart Attributes file for current time
	write_smart_attributes()

	# Get set of Smart Attributes to report on
	# (current, previous, baseline)
	# may be None
	run_list = read_logs(drive_directory)

	drive_info = read_info(drive_directory)

	EmailBodyGenerator().generate(run_list, drive_info, get_drive_name())

	send_email()


def initialize(hdd_path):
	# create config file if doesn't exist.
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
	if not os.path.exists(os.path.join(package_directory, "config.ini")):
		with open(os.path.join(package_directory, './config.ini'), 'w+') as configfile:
			config.write(configfile)

	# create folder structure
	global drive_path
	drive_path = hdd_path
	history_directory = os.path.join(package_directory, "./history")
	if not os.path.exists(history_directory):
		os.mkdir(history_directory)

	# each hard drive has its own folder to store logs
	global drive_directory
	drive_directory = history_directory + "/" + get_drive_name()
	if not os.path.exists(drive_directory):
		os.mkdir(drive_directory)


def write_drive_info():
	info_file_name = drive_directory + "/info.txt"

	output = run_command("sudo smartctl -i " + drive_path)

	with open(info_file_name, "w+b") as f:
		f.write(output)


def write_smart_attributes():
	now = datetime.datetime.now()
	filename = drive_directory + "/" + now.strftime("SmartAttributes_%Y_%m_%d_%H_%M_%S")

	output = run_command("sudo smartctl --attributes " + drive_path)

	with open(filename, "w+b") as f:
		f.write(output)


def send_email():
	body = get_email_body()
	#with open(os.path.join(package_directory, './email.html'), "w+") as f:
	#	f.write(body)

	config = configparser.ConfigParser()
	config.read(os.path.join(package_directory, 'config.ini'))

	msg = MIMEMultipart('alternative')
	msg.attach(MIMEText(body, 'html'))
	msg['Subject'] = "SmartCheck results for " + get_drive_name()
	msg['From'] = config['MAIL']['FROM']
	msg['To'] = config['MAIL']['TO']

	try:
		if config['MAIL'].getboolean('USE_SSL'):
			server = smtplib.SMTP_SSL(config['MAIL']['SERVER'], config['MAIL']['PORT'])
		else:
			server = smtplib.SMTP(config['MAIL']['SERVER'] + ':' + config['MAIL']['PORT'])

		server.ehlo()

		if config['MAIL'].getboolean('USE_TLS'):
			server.starttls()

		server.login(config['MAIL']['USERNAME'], config['MAIL']['PASSWORD'])
		server.send_message(msg)
		server.quit()
	except Exception:
		print('Failed to send email.')
		raise


def get_email_body():
	dir = os.path.join(package_directory, "foundation.emails/dist/")
	file_listing = os.listdir(dir)
	expression = 'smart-notification_' + get_drive_name() + '(.*?)'
	regex = compile(expression)
	filtered = [i for i in file_listing if regex.search(i)]
	filtered.sort()
	# get most recently generated html file
	filename = dir + filtered[-1]

	with open(filename, "r") as f:
		data = f.read()
	return data


def read_logs(drive_directory):
	file_listing = os.listdir(drive_directory)
	file_listing.remove("info.txt")
	file_listing.sort()

	if len(file_listing) == 0:
		print("baseline: empty")
		print("previous: empty")
		print("current: empty")
		return None, None, None
	elif len(file_listing) == 1:
		print("baseline: empty")
		print("previous: empty")
		print("current: %s" % (file_listing[0]))
		return extract_attributes(drive_directory + '/' + file_listing[0]), None, None
	elif len(file_listing) == 2:
		print("baseline: %s" % (file_listing[0]))
		print("previous: empty")
		print("current: %s" % (file_listing[1]))
		return extract_attributes(drive_directory + '/' + file_listing[1]), None, \
				extract_attributes(drive_directory + '/' + file_listing[0])

	print("baseline: %s" % (file_listing[0]))
	baseline = extract_attributes(drive_directory + '/' + file_listing[0])
	print("previous: %s" % (file_listing[-2]))
	previous = extract_attributes(drive_directory + '/' + file_listing[-2])
	print("current: %s" % (file_listing[-1]))
	current = extract_attributes(drive_directory + '/' + file_listing[-1])

	return current, previous, baseline


def read_info(drive_directory):
	data = []
	with open(drive_directory + "/info.txt", "r") as f:
		for i, line in enumerate(f):
			# disregard header information in file
			if i > 3 and line.strip():
				data.append(line.split(":")[1].strip())
	return Info(data)


# Read relevant rows of file and return Run object
def extract_attributes(file_path):
	my_attributes = []
	with open(file_path, "r") as f:
		for i, line in enumerate(f):
			# disregard header information in file
			if i > 6 and line.strip():
				my_attributes.append(Attribute(extract_attribute_values(line)))
	return Run(my_attributes, datetime.datetime.now())


# String split method that handles whitespace in last column (Min/Max X)
def extract_attribute_values(line):
	values = line.split()
	# there should only be 10 columns
	# assume no issues with whitespace on the first 9 columns
	while len(values) > 10:
		values[9] += " " + values[10]
		values.pop(10)
	return values


def run_command(command):
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	(output, err) = process.communicate()
	return output


# For readability
def get_drive_name():
	return drive_path.split("/")[-1]