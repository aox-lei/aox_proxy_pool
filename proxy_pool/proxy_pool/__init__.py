# -*- coding: utf-8 -*-
import logging
import configparser

logging.basicConfig(
    level=logging.DEBUG,
    format=
    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

config = configparser.ConfigParser()
config.read('config.ini')