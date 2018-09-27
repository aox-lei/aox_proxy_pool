# -*- coding: utf-8 -*-
import os
from proxy_pool import Session
from proxy_pool.models import Ip


def update_squid_conf(default_conf_path, conf_path):
    session = Session()
    try:
        proxy_list = session.query(Ip).filter(Ip.score > 0).filter(
            Ip.weight > 0).order_by(Ip.weight.desc()).with_entities(
                Ip.id, Ip.ip, Ip.port, Ip.score).limit(100).all()
    except Exception:
        return False
    proxy_conf = ''
    for _info in proxy_list:
        proxy_conf += 'cache_peer %s parent %d 0 no-query weighted-round-robin weight=%d connect-fail-limit=2 allow-miss max_conn=2 name=proxy-%d\n' % (
            _info.ip, _info.port, _info.score, _info.id)

    with open(default_conf_path, 'r') as f:
        default_conf = f.read()
    conf = default_conf + '\n' + proxy_conf
    with open(conf_path, 'w') as f:
        f.write(conf)
    os.system('squid -k reconfig')
    print('sync success')
