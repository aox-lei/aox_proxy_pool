# -*- coding: utf-8 -*-
import scrapy
from proxy_pool.items import ProxyPoolItem


class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['www.xicidaili.com']
    CURRENT_PAGE = 1

    def parse(self, response):
        ip_list = response.css('#ip_list > tr')
        for _ip_info in ip_list:
            _ip = _ip_info.css('td:nth-child(2)::text').extract()
            _port = _ip_info.css('td:nth-child(3)::text').extract()
            _http_type = _ip_info.css('td:nth-child(6)::text').extract()
            if not _ip or not _port or not _http_type:
                continue
            item = ProxyPoolItem()
            item['ip'] = _ip[0]
            item['port'] = int(_port[0])
            item['http_type'] = 1 if _http_type[0] == 'HTTP' else 2
            yield item
        if self.CURRENT_PAGE < 5:
            self.CURRENT_PAGE += 1
            yield scrapy.Request('http://www.xicidaili.com/nn/' +
                                 str(self.CURRENT_PAGE))

    def start_requests(self):
        yield scrapy.Request('http://www.xicidaili.com/nn/' +
                             str(self.CURRENT_PAGE))
