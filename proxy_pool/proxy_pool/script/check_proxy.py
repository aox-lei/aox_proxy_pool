# -*- coding: utf-8 -*-
import requests
import arrow
import time
import logging
import re
import logging
from concurrent.futures import ThreadPoolExecutor
from proxy_pool import Session
from proxy_pool.models import Ip
from proxy_pool import utils


class check_proxy(object):
    check_urls_str = {
        'http://www.baidu.com': '百度',
        'http://www.qq.com': '腾讯',
        'http://www.ccidcom.com/': '通信',
        'https://www.taobao.com/': '淘宝',
        'https://www.zhihu.com/': '知乎',
        'https://weibo.com/': '微博',
        'https://www.baidu.com': '百度',
    }
    check_urls = {
        'http': [
            'http://www.baidu.com', 'http://www.qq.com',
            'http://www.ccidcom.com/'
        ],
        'https': [
            'https://www.taobao.com/', 'https://www.zhihu.com/',
            'https://weibo.com/', 'https://www.baidu.com'
        ]
    }

    check_ports = {
        80: 5,
        8080: 1,
        3128: 1,
        8081: 1,
        9080: 1,
        1080: 1,
        21: 3,
        23: 2,
        53: 3,
        1863: 2,
        2289: 1,
        443: 5,
        69: 1,
        22: 5,
        25: 2,
        110: 2,
        7001: 1,
        9090: 1,
        3389: 5,
        1521: 5,
        1158: 3,
        2100: 1,
        1433: 2,
        3306: 5,
        5631: 1,
        5632: 1,
        5000: 2,
        8888: 2
    }

    def run(self):
        while 1:
            ip_list = self.get_proxy_list()
            if (not ip_list):
                return False
            pool = ThreadPoolExecutor(max_workers=100)

            threads = []
            for _info in ip_list:
                threads.append(
                    pool.submit(self.check_ip, _info.ip, _info.port,
                                _info.http_type, _info.score))

            pool.shutdown()

    def get_proxy_list(self):
        session = Session()
        try:
            lists = session.query(Ip).filter(Ip.score > 0).order_by(
                Ip.update_time.desc()).with_entities(
                    Ip.id, Ip.ip, Ip.port, Ip.http_type, Ip.score).all()
            return lists
        except Exception as e:
            logging.exception(e)
            return False

    def check_ip(self, ip, port, http_type, score):
        open_ports = self.check_port(ip, port)
        session = Session()
        if open_ports is False:
            try:
                session.query(Ip).filter(Ip.ip == ip).filter(
                    Ip.port == port).update({
                        'score': 0,
                        'update_time': arrow.now().datetime
                    })
                session.commit()
            except Exception as e:
                logging.exception(e)
                session.rollback()
            logging.warning('%s:%d ---- 端口未开放' % (ip, int(port)))
            return False

        speed_time = self.check_visit(ip, port, http_type)
        if speed_time is False:
            try:
                session.query(Ip).filter(Ip.ip == ip).filter(
                    Ip.port == port).update({
                        'score':
                        score - 1 if score - 1 >= 0 else 0,
                        'open_port':
                        ','.join(map(lambda x:str(x), open_ports)),
                        'update_time':
                        arrow.now().datetime
                    })
                session.commit()
            except Exception as e:
                logging.exception(e)
                session.rollback()

            logging.warning('%s:%d ------ 无法访问' % (ip, int(port)))
        else:
            try:
                score = score + 1 if score + 1 <= 5 else 5
                session.query(Ip).filter(Ip.ip == ip).filter(
                    Ip.port == port).update({
                        'score':
                        score,
                        'speed':
                        speed_time,
                        'weight':
                        self.calculate_weight(score, speed_time, open_ports),
                        'open_port':
                        ','.join(map(lambda x:str(x), open_ports)),
                        'update_time':
                        arrow.now().datetime,
                    })
                session.commit()
            except Exception as e:
                logging.exception(e)
                session.rollback()

            logging.info('%s:%d ------ 代理有效, speed:%d, open_ports:%s' %
                         (ip, port, speed_time, ','.join(open_ports)))

    def check_visit(self, ip, port, http_type):
        if http_type == 1:
            check_urls = self.check_urls['http']
        elif http_type == 2:
            check_urls = self.check_urls['https']
        elif http_type == 3:
            check_urls = self.check_urls['http'] + self.check_urls['https']

        total_speed_time = 0
        visit_success_count = 0
        for _url in check_urls:
            _start_time = time.time()
            try:
                result = requests.get(_url, timeout=5)
                if self.check_html_title(result.html,
                                         self.check_urls_str.get(_url)):
                    total_speed_time = int((time.time() - _start_time) * 1000)
                    visit_success_count += 1
            except Exception as e:
                pass

        if total_speed_time == 0 or visit_success_count == 0:
            return False
        else:
            return int(total_speed_time / visit_success_count)

    def check_html_title(self, html, check_str):
        title = re.findall('<title>(.*?)<\/title>', html)
        if title and check_str in title[0]:
            return True
        else:
            return False

    def check_port(self, ip, port):
        check_ports = list(self.check_ports.keys())
        check_ports.append(port)
        check_ports = list(set(check_ports))

        ok_ports = []
        for _port in check_ports:
            if utils.check_port(ip, _port):
                ok_ports.append(_port)

        if port not in ok_ports:
            return False
        return ok_ports

    def calculate_weight(self, score, speed_time, open_ports):
        _weight += score
        for _port in open_ports:
            if _port in self.check_ports:
                _weight += self.check_ports.get(_port)
            else:
                _weight += 1

        _weight += 10000 - speed_time

        return _weight
