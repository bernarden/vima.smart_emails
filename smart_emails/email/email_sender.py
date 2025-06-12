import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from smart_emails.helpers.settings import Settings


class EmailSender:
	def __init__(self, settings: Settings):
		self.settings = settings

	def send_html_email(self, subject: str, body: str) -> None:
		msg = MIMEMultipart('alternative')
		msg.attach(MIMEText(body, 'html'))
		msg['Subject'] = subject
		msg['From'] = self.settings.mail_from
		msg['To'] = self.settings.mail_to

		try:
			host = self.settings.mail_server
			port = self.settings.mail_port
			server_connection = smtplib.SMTP_SSL(host, port) if self.settings.mail_use_ssl else smtplib.SMTP(host, port)
			server_connection.ehlo()

			if self.settings.mail_use_tls:
				server_connection.starttls()

			server_connection.login(self.settings.mail_username, self.settings.mail_password)
			server_connection.send_message(msg)
			server_connection.quit()
		except Exception:
			print('Failed to send the email.')
			raise
