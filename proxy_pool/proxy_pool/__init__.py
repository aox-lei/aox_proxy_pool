# -*- coding: utf-8 -*-
import logging
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
logging.basicConfig(
    level=logging.DEBUG,
    format=
    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

config = configparser.ConfigParser()
config.read('config.ini')

engine = create_engine(config.get('mysql', 'dsn'), echo=False)
Session = sessionmaker(engine)
