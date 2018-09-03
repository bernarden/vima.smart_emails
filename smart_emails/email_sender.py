import smtplib
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smart_emails.constants import Constants


class EmailSender:

	@staticmethod
	def send_html_email(subject: str, body: str) -> None:
		config = configparser.ConfigParser()
		config.read(Constants.instance().config_file_path)

		msg = MIMEMultipart('alternative')
		msg.attach(MIMEText(body, 'html'))
		msg['Subject'] = subject
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
