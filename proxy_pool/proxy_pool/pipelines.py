# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import arrow
from proxy_pool import connect


class ProxyPoolPipeline(object):
    def process_item(self, item, spider):
        if not self.check(item['ip'], item['port']):
            session = connect.cursor()
            session.execute(
                'INSERT INTO ip (ip, port, http_type, score, create_time, update_time) VALUES ("%s", %d, %d, 5, "%s", "%s")'
                % (item['ip'], item['port'], item['http_type'],
                   arrow.now().format('YYYY-MM-DD HH:mm:ss'),
                   arrow.now().format('YYYY-MM-DD HH:mm:ss')))
            connect.commit()

    def check(self, ip, port):
        session = connect.cursor()
        session.execute(
            'SELECT id from ip WHERE ip="%s" and port="%s"' % (ip, port))
        if session.fetchone():
            return True
        return False
