from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(TEXT)
    email = Column(TEXT)
    code = Column(String(6))
    time = Column(Integer)
