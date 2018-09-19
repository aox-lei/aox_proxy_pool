# -*- coding: utf-8 -*-
import configparser
from hot_redis import HotClient, configure

config = configparser.ConfigParser()
config.read('config.ini')

configure(
    host=config.get('redis', 'host'),
    port=config.getint('redis', 'port'),
    db=config.getint('redis', 'db'))
