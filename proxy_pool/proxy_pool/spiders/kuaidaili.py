# -*- coding: utf-8 -*-
import scrapy
import time
from proxy_pool.items import ProxyPoolItem


class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'
    allowed_domains = ['www.kuaidaili.com']
    CURRENT_PAGE = 1

    def parse(self, response):
        ip_list = response.css('#list > table > tbody > tr')
        for _ip_info in ip_list:
            _ip = _ip_info.css('td:nth-child(1)::text').extract()
            _port = _ip_info.css('td:nth-child(2)::text').extract()
            _http_type = _ip_info.css('td:nth-child(4)::text').extract()

            if not _ip or not _port or not _http_type:
                continue
            item = ProxyPoolItem()
            item['ip'] = _ip[0].strip()
            item['port'] = int(_port[0].strip())
            item['http_type'] = 1 if _http_type[0].strip() == 'HTTP' else 2
            item['country'] = 'CN'
            yield item

        if self.CURRENT_PAGE < 5:
            self.CURRENT_PAGE += 1
            time.sleep(1)
            yield scrapy.Request('https://www.kuaidaili.com/free/inha/' +
                                 str(self.CURRENT_PAGE))

    def start_requests(self):
        yield scrapy.Request('https://www.kuaidaili.com/free/inha/')
