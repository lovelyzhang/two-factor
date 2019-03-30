import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth_server.config import DB_PATH
from auth_server.models import Base, User
from auth_server.log import AUTH_LOGGER

engine = create_engine('sqlite:///{}'.format(DB_PATH))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


def find_user(username):
    session = DBSession()
    user = session.query(User).filter(User.username == username).first()
    return user


def update_user_code(username, code):
    ok = False
    session = DBSession()
    try:
        mapped_values = {
            "code": code,
            "time": int(time.time())
        }
        session.query(User).filter(User.username == username).update(mapped_values)
        session.commit()
        ok = True
    except Exception as e:
        AUTH_LOGGER.exception(e)
        session.rollback()
    return ok
