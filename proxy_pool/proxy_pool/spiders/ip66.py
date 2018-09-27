# -*- coding: utf-8 -*-
import scrapy
import time
import re
from scrapy.linkextractors import LinkExtractor
from proxy_pool.items import ProxyPoolItem


class Ip66Spider(scrapy.Spider):
    name = 'ip66'
    allowed_domains = ['www.66ip.cn']
    CURRENT_PAGE = 1

    def parse(self, response):
        link = LinkExtractor(restrict_css='ul.textlarge22', allow='areaindex')
        links = link.extract_links(response)
        for _link in links:
            # yield scrapy.Request('http://www.66ip.cn/areaindex_1/1.html', callback=self.parse_list)
            yield scrapy.Request(_link.url, callback=self.parse_list)

    def start_requests(self):
        yield scrapy.Request('http://www.66ip.cn/')

    def parse_list(self, response):
        ip_list = response.css('#footer > div > table > tr')

        for _ip_info in ip_list:
            _ip = _ip_info.css('td:nth-child(1)::text').extract()
            _port = _ip_info.css('td:nth-child(2)::text').extract()

            if not _ip or not _port:
                continue

            if _ip[0].strip() == 'ip':
                continue
            item = ProxyPoolItem()
            item['ip'] = _ip[0].strip()
            item['port'] = int(_port[0].strip())
            item['http_type'] = 3
            item['country'] = 'CN'
            yield item
        now_page = re.findall('.*?\/(\d+)\.html', response._url)
        if now_page:
            now_page = int(now_page[0])

            if now_page < 5:
                yield scrapy.Request(
                    response._url.replace('%d.html' % (now_page),
                                          '%d.html' % (now_page + 1)), callback=self.parse_list)
            time.sleep(1)
