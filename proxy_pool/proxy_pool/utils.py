# -*- coding: utf-8 -*-
import socket
import os
def check_port(ip, port, timeout=5):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(timeout)
    is_open = True
    try:
        sk.connect((ip,port))
    except Exception:
        is_open = False
    sk.close()
    return is_open

def check_network():
    exit_code = os.system('ping www.baidu.com -c 4 > /dev/null 2>&1')
    if exit_code:
        return False
    return True