# -*- coding: utf-8 -*-
import logging
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class Ip(Base):
    __tablename__ = 'ip'

    id = Column(Integer, primary_key=True)
    ip = Column(String(length=15), default='')
    port = Column(Integer, default=0)
    score = Column(Integer, default=5)
    weight = Column(Integer, default=0)
    speed = Column(Integer, default=0)
    http_type = Column(Integer, default=1)
    country = Column(Integer, default='')
    open_port = Column(String(length=255), default='')
    create_time = Column(DateTime, default='0000-00-00 00:00:00')
    update_time = Column(DateTime, default='0000-00-00 00:00:00')
