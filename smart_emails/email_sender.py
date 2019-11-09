import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smart_emails.helpers.configAccessor import ConfigAccessor


class EmailSender:

    @staticmethod
    def send_html_email(subject: str, body: str) -> None:
        config = ConfigAccessor()

        msg = MIMEMultipart('alternative')
        msg.attach(MIMEText(body, 'html'))
        msg['Subject'] = subject
        msg['From'] = config.get('MAIL.FROM')
        msg['To'] = config.get('MAIL.TO')

        try:
            if config.get_boolean('MAIL.USE_SSL'):
                server = smtplib.SMTP_SSL(config.get('MAIL.SERVER'), config.get('MAIL.PORT'))
            else:
                server = smtplib.SMTP(config.get('MAIL.SERVER') + ':' + config.get('MAIL.PORT'))

            server.ehlo()

            if config.get_boolean('MAIL.USE_TLS'):
                server.starttls()

            server.login(config.get('MAIL.USERNAME'), config.get('MAIL.PASSWORD'))
            server.send_message(msg)
            server.quit()
        except Exception:
            print('Failed to send email.')
            raise
