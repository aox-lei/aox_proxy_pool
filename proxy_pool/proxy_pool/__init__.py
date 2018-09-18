# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data/test.db?check_same_thread=False')
create_session = sessionmaker(bind=engine)