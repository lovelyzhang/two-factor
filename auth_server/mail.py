import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from auth_server.utils import generate_code
from auth_server.log import AUTH_LOGGER
from auth_server.config import TPL_PATH, TIMEOUT
from auth_server.config import MAIL_HOST, MAIL_PASSWD, MAIL_PORT, MAIL_USER_NAME


def render_code(code):
    j2_env = Environment(loader=FileSystemLoader(TPL_PATH),
                         trim_blocks=True)

    return j2_env.get_template('code.html').render(code=code)


class LocalMailSerivce(object):
    def __init__(self, host, port, username, passwd):
        self._host = host
        self._port = port
        self._username = username
        self._passwd = passwd

    def _send_mail_to_receiver(self, receiver, msg):
        ok = False
        try:
            _server = smtplib.SMTP(host=self._host, port=self._port, timeout=TIMEOUT)
            # Puts the connection to the SMTP server into TLS mode.
            _server.starttls()
            _server.login(self._username, self._passwd)
            _server.sendmail(from_addr=self._username, to_addrs=[receiver], msg=msg.as_string())
            _server.quit()
            ok = True
        except smtplib.SMTPServerDisconnected as e:
            AUTH_LOGGER.error("mail server connect timeout.")
            AUTH_LOGGER.exception(e)
        except smtplib.SMTPException as e:
            AUTH_LOGGER.error("send mail failed.")
            AUTH_LOGGER.exception(e)
        return ok

    def send_verify_code(self, receiver):
        message = MIMEMultipart('alternative')
        message['Subject'] = '验证码'
        message['From'] = self._username
        message['To'] = receiver
        message.preamble = "verify code"
        code = generate_code()
        html = render_code(code)
        part = MIMEText(html, 'html', 'utf-8')
        message.attach(part)
        if not self._send_mail_to_receiver(receiver, message):
            return None
        return code


class MailSerivceFactory(object):
    """MailSerivceFactory"""

    def __init__(self, service=LocalMailSerivce, **kwargs):
        self._kwargs = kwargs
        self._service = service

    def send_verify_code(self, receiver):
        _mail_service = self._service(**self._kwargs)
        return _mail_service.send_verify_code(receiver)


MAIL_SERVICE = LocalMailSerivce(MAIL_HOST, MAIL_PORT, MAIL_USER_NAME, MAIL_PASSWD)

if __name__ == '__main__':
    pass
