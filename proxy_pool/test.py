# -*- coding: utf-8 -*-
import arrow
from proxy_pool import connect
item = {}
item['ip'] = '1.1.1.1'
item['port'] = 80
item['http_type'] = 1
session = connect.cursor()
# session.execute(
#     'INSERT INTO ip (ip, port, http_type, score, create_time, update_time) VALUES ("%s", %d, %d, 5, "%s", "%s")'
#     % (item['ip'], item['port'], item['http_type'],
#        arrow.now().format('YYYY-MM-DD HH:mm:ss'),
#        arrow.now().format('YYYY-MM-DD HH:mm:ss')))

session.execute('SELECT * from ip')
print(session.fetchall())
connect.commit()
connect.close()