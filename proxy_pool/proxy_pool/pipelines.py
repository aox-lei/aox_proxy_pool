# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import arrow
from proxy_pool import create_session
from sqlalchemy.orm.exc import NoResultFound
from proxy_pool.model import Ip


class ProxyPoolPipeline(object):
    def process_item(self, item, spider):
        if not self.check(item['ip'], item['port']):
            now_datetime = arrow.now().datetime
            ip_object = Ip(
                ip=item['ip'],
                port=item['port'],
                http_type=item['http_type'],
                speed=0,
                score=5,
                create_time=now_datetime,
                update_time=now_datetime)
            session = create_session()
            try:
                session.add(ip_object)
                session.commit()
                session.close()
            except Exception as e:
                print(e)
                session.rollback()
                session.close()

    def check(self, ip, port):
        session = create_session()
        try:
            ip_info = session.query(Ip).filter(Ip.ip == ip).filter(
                Ip.port == port).with_entities(Ip.id).one()
            session.close()
            if ip_info:
                return True
        except Exception:
            session.close()
            return False
