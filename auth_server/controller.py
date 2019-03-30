import time
from auth_server.config import SUCCESS, ERROR
from auth_server.db import find_user, update_user_code
from auth_server.mail import MAIL_SERVICE
from auth_server.log import AUTH_LOGGER


def send_code(username):
    user = find_user(username)
    if not user:
        AUTH_LOGGER.error("not find user:{}".format(username))
        return ERROR
    now = int(time.time())
    if user.code and abs(now - user.time) < 300:
        AUTH_LOGGER.error("username:{},no need new code".format(username))
        return SUCCESS
    else:
        code = MAIL_SERVICE.send_verify_code(user.email)
        if not code:
            AUTH_LOGGER.error("username:{},no send mail".format(username))
            return ERROR
        if not update_user_code(username, code):
            return ERROR
    return SUCCESS


def verify_code(username, code):
    user = find_user(username)
    if not user:
        AUTH_LOGGER.error("not find user:{}".format(username))
        return ERROR
    now = int(time.time())
    if abs(user.time - now) > 300:
        AUTH_LOGGER.error("username:{},verify time out".format(username))
        return ERROR
    if code != user.code:
        AUTH_LOGGER.error("username:{},verify code error".format(username))
        return ERROR
    return SUCCESS
