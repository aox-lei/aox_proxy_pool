# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import arrow
from proxy_pool import Session
from proxy_pool.models import Ip
from sqlalchemy.orm.exc import NoResultFound


class ProxyPoolPipeline(object):
    def process_item(self, item, spider):
        if not self.check(item['ip'], item['port']):
            session = Session()
            try:
                session.add(
                    Ip(ip=item['ip'],
                       port=item['port'],
                       http_type=item['http_type'],
                       country=item['country'],
                       create_time=arrow.now().datetime,
                       update_time=arrow.now().datetime))
                session.commit()
            except Exception as e:
                session.rollback()

    def check(self, ip, port):
        session = Session()
        try:
            info = session.query(Ip).filter(Ip.ip == ip).filter(
                Ip.port==port).with_entities(Ip.id).one()
        except NoResultFound as e:
            return False

        return True