# -*- coding: utf-8 -*-
import requests
import arrow
from concurrent.futures import ThreadPoolExecutor
from proxy_pool import create_session
from proxy_pool.model import Ip


class check_proxy(object):
    check_url = [
        'http://www.baidu.com', 'http://www.qq.com', "https://www.taobao.com/",
        "https://www.zhihu.com/"
    ]

    def run(self):
        while 1:
            ip_list = self.get_proxy_list()
            pool = ThreadPoolExecutor()

            threads = []
            for _info in ip_list:
                threads.append(
                    pool.submit(self.check_ip, _info.ip, _info.port,
                                _info.http_type, _info.score))

            pool.shutdown()

    def get_proxy_list(self):
        session = create_session()
        try:
            ip_list = session.query(Ip).with_entities(
                Ip.ip, Ip.port, Ip.http_type, Ip.score).order_by(
                    Ip.update_time).limit(100).all()

            return ip_list
        except Exception:
            return False

    def check_ip(self, ip, port, http_type, score):
        if http_type == 1:
            proxy_ip = 'http://' + ip + ':' + str(port)
        else:
            proxy_ip = 'https://' + ip + ':' + str(port)
        right_time = 0
        for _url in self.check_url:
            try:
                result = requests.get(
                    _url,
                    proxies={
                        'http': proxy_ip,
                        'https': proxy_ip
                    },
                    timeout=5)
                if result.status_code == 200:
                    right_time += 1
            except Exception:
                pass

        session = create_session()

        try:
            if right_time >= len(self.check_url) / 2:
                session.query(Ip).filter(Ip.ip == ip).filter(
                    Ip.port == port).update({
                        'update_time':
                        arrow.now().datetime,
                        'score':
                        5 if score + 1 >= 5 else score + 1
                    })
            else:
                if score == 1:
                    session.query(Ip).filter(Ip.ip == ip).filter(
                        Ip.port == port).delete()
                else:
                    session.query(Ip).filter(Ip.ip == ip).filter(
                        Ip.port == port).update({
                            'update_time':
                            arrow.now().datetime,
                            'score':
                            score - 1
                        })

            session.commit()
            session.close()
        except Exception:
            session.rollback()
            session.close()

        print('%s:%d ----- 检测完成' % (ip, port))
