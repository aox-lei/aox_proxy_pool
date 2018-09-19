# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime

Base = declarative_base()


class Ip(Base):
    __tablename__ = 'ip'

    id = Column(Integer, primary_key=True)
    ip = Column(String(15))
    port = Column(Integer)
    http_type = Column(Integer)
    speed = Column(Integer)
    score = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)