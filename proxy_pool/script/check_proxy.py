# -*- coding: utf-8 -*-
import requests
import arrow
import time
from concurrent.futures import ThreadPoolExecutor
from proxy_pool import create_session
from proxy_pool.model import Ip


class check_proxy(object):
    check_url = {
        'http': [
            'http://www.baidu.com', 'http://www.qq.com',
            "http://www.ccidcom.com/"
        ],
        'https': [
            'http://www.baidu.com', 'http://www.qq.com',
            "http://www.ccidcom.com/", "https://www.taobao.com/",
            "https://www.zhihu.com/", "https://weibo.com/",
            "https://www.baidu.com"
        ]
    }

    def run(self):
        while 1:
            ip_list = self.get_proxy_list()
            pool = ThreadPoolExecutor(max_workers=100)

            threads = []
            for _info in ip_list:
                threads.append(
                    pool.submit(self.check_ip, _info.ip, _info.port,
                                _info.http_type, _info.score))

            pool.shutdown()

    def get_proxy_list(self):
        session = create_session()
        try:
            ip_list = session.query(Ip).filter(Ip.score > 0).with_entities(
                Ip.ip, Ip.port, Ip.http_type,
                Ip.score).order_by(Ip.update_time).limit(1000).all()

            return ip_list
        except Exception:
            return False

    def check_ip(self, ip, port, http_type, score):
        if http_type == 1:
            proxies = {'http': 'http://' + ip + ':' + str(port)}
            check_url = self.check_url['http']
        else:
            proxies = {'https': 'http://' + ip + ':' + str(port)}
            check_url = self.check_url['https']

        right_time = 0
        speed_time_total = 0
        speed_time = 0
        for _url in check_url:

            try:
                _start_time = int(round(time.time()) * 1000)
                result = requests.get(_url, proxies=proxies, timeout=5)
                if result.status_code == 200:
                    right_time += 1
                    speed_time_total += int(round(
                        time.time() * 1000)) - _start_time

            except Exception:
                pass
        if right_time > 0 and speed_time_total > 0:
            speed_time = int(speed_time_total / right_time)

        session = create_session()

        try:
            if right_time >= len(self.check_url) / 2:
                session.query(Ip).filter(Ip.ip == ip).filter(
                    Ip.port == port).update({
                        'update_time':
                        arrow.now().datetime,
                        'score':
                        5 if score + 1 >= 5 else score + 1,
                        'speed':
                        speed_time
                    })
                print('%s:%d ----- 有效' % (ip, port))
            else:
                session.query(Ip).filter(Ip.ip == ip).filter(
                    Ip.port == port).update({
                        'update_time':
                        arrow.now().datetime,
                        'score':
                        score - 1,
                        'speed':
                        speed_time
                    })
                print('%s:%d ----- 失效' % (ip, port))

            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            session.close()
            print(e)
