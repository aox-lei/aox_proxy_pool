# -*- coding: utf-8 -*-
import socket

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