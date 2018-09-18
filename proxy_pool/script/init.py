# -*- coding: utf-8 -*-
from proxy_pool import engine
from proxy_pool.model import Base, Ip


def init():
    Base.metadata.create_all(engine)