# -*- coding: utf-8 -*-
import logging
import configparser
from hot_redis import configure
logging.basicConfig(
    level=logging.DEBUG,
    format=
    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

config = configparser.ConfigParser()
config.read('config.ini')
configure(
    host=config.get('redis', 'host'),
    port=config.getint('redis', 'port'),
    db=config.getint('redis', 'db'))
