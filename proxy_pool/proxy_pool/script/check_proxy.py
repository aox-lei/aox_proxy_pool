# -*- coding: utf-8 -*-
import requests
import arrow
import time
import logging
import re
import logging
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import ConnectionError
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
        'https://www.baidu.com': '百度',
    }
    check_urls = {
        'http': [
            'http://www.baidu.com', 'http://www.qq.com',
            'http://www.ccidcom.com/'
        ],
        'https': [
            'https://www.taobao.com/', 'https://www.zhihu.com/',
            'https://www.baidu.com'
        ]
    }

    check_ports = {
        80: 500,
        8080: 100,
        3128: 100,
        8081: 100,
        9080: 100,
        1080: 100,
        21: 300,
        23: 200,
        53: 300,
        1863: 200,
        2289: 100,
        443: 500,
        69: 100,
        22: 500,
        25: 200,
        110: 200,
        7001: 100,
        9090: 100,
        3389: 500,
        1521: 500,
        1158: 300,
        2100: 100,
        1433: 200,
        3306: 500,
        5631: 100,
        5632: 100,
        5000: 200,
        8888: 200
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
                    pool.submit(
                        self.check_ip,
                        _info.ip,
                        _info.port,
                        _info.http_type,
                        _info.score,
                        is_new=1
                        if _info.create_time == _info.update_time else 0))

            pool.shutdown()

    def get_proxy_list(self):
        session = Session()
        try:
            lists = session.query(Ip).filter(Ip.score > 0).order_by(
                Ip.update_time.desc()).with_entities(
                    Ip.id, Ip.ip, Ip.port, Ip.http_type, Ip.score,
                    Ip.create_time, Ip.update_time).all()
            return lists
        except Exception as e:
            logging.exception(e)
            return False

    def check_ip(self, ip, port, http_type, score, is_new=1):
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

        _update_data = {
            'open_port': ','.join(map(lambda x: str(x), open_ports)),
            'update_time': arrow.now().datetime
        }
        if is_new == 1:
            new_http_type = self.check_http_type(ip, port)
            if (new_http_type):
                _update_data['http_type'] = new_http_type

        speed_time = self.check_visit(ip, port, http_type)

        if speed_time is False:
            _update_data['score'] = score - 1 if score - 1 >= 0 else 0

            logging.warning('%s:%d ------ 无法访问' % (ip, int(port)))
        else:
            _update_data['score'] = score + 1 if score + 1 <= 5 else 5
            _update_data['speed'] = speed_time
            _update_data['weight'] = self.calculate_weight(
                score, speed_time, open_ports)

            logging.info('%s:%d ------ 代理有效, speed:%d, open_ports:%s' %
                         (ip, port, speed_time, _update_data['open_port']))

        try:
            session.query(Ip).filter(Ip.ip == ip).filter(
                Ip.port == port).update(_update_data)
            session.commit()
        except Exception as e:
            logging.exception(e)
            session.rollback()

    def check_http_type(self, ip, port):
        check_urls = self.check_urls['http'] + self.check_urls['https']
        success_visit_count = {
            'http': len(self.check_urls['http']),
            'https': len(self.check_urls['https'])
        }
        for _url in check_urls:
            try:
                requests.get(
                    _url,
                    timeout=5,
                    proxies={
                        'http': 'http://%s:%d' % (ip, port),
                        'https': 'http://%s:%d' % (ip, port)
                    })
            except ConnectionError:
                if _url[0:5] == 'https':
                    success_visit_count['https'] -= 1
                elif _url[0:4] == 'http':
                    success_visit_count['http'] -= 1
            except Exception:
                pass

        if success_visit_count['http'] > 0 and success_visit_count[
                'https'] == 0:
            return 1
        elif success_visit_count['https'] > 0 and success_visit_count[
                'http'] == 0:
            return 2
        elif success_visit_count['https'] > 0 and success_visit_count['http'] > 0:
            return 3
        else:
            return False

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
                result = requests.get(
                    _url,
                    timeout=5,
                    proxies={
                        'http': 'http://%s:%d' % (ip, port),
                        'https': 'http://%s:%d' % (ip, port)
                    })

                if self.check_html_title(result.text,
                                         self.check_urls_str.get(_url)):
                    total_speed_time += int((time.time() - _start_time) * 1000)
                    visit_success_count += 1
            except Exception:
                pass

        if total_speed_time == 0 or visit_success_count == 0:
            return False
        else:
            total_speed_time += (len(check_urls) - visit_success_count) * 5000
            visit_success_count = len(check_urls)

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
        _weight = score * 1000
        for _port in open_ports:
            if _port in self.check_ports:
                _weight += self.check_ports.get(_port)
            else:
                _weight += 1

        _weight += 10000 - speed_time

        return _weight
