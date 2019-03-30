import os
from auth_server.excepts import AuthServerBaseException

# return code
SUCCESS = '0'
ERROR = '1'

# base directory path
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# db directory
DB_PATH = os.path.join(BASE_PATH, "db/auth.db")

# template directory
TPL_PATH = os.path.join(BASE_PATH, "tpl")

# connect timeout
TIMEOUT = 120

# email username
MAIL_USER_NAME = os.environ.get("MAIL_USER_NAME")

if MAIL_USER_NAME is None:
    raise AuthServerBaseException("mail config error: MAIL_USER_NAME is None")
# email passwd
MAIL_PASSWD = os.environ.get("MAIL_PASSWD")

if MAIL_PASSWD is None:
    raise AuthServerBaseException("mail config error: MAIL_PASSWD is None")
# email host
MAIL_HOST = os.environ.get("MAIL_HOST")

if MAIL_HOST is None:
    raise AuthServerBaseException("mail config error: MAIL_HOST is None")
# email port
MAIL_PORT = os.environ.get("MAIL_PORT")
if MAIL_PORT is None:
    raise AuthServerBaseException("mail config error: MAIL_PORT is None")
